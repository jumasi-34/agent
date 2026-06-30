# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import os
import re
import sys
import urllib.parse
from typing import List, Dict, Tuple

# =========================================================================
# SECTION 2. Constants & Configuration (상수 및 정규식 설정)
# =========================================================================
# 비표준 이중 대괄호 링크 검출용 정규식 (예: [[link_name]])
DOUBLE_BRACKET_RE = re.compile(r'\[\[(.*?)\]\]')

# 순수 본문 내 마크다운 표준 링크 검출용 정규식 (예: [display_text](path))
LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


# =========================================================================
# SECTION 3. Core Verification Logic (핵심 검증 및 파싱 함수)
# =========================================================================

def remove_code_elements(content: str) -> str:
    """마크다운 본문에서 펜스드 코드 블록(Fenced Code Blocks) 및 인라인 코드(백틱 영역)를 공백으로 대체합니다.

    줄바꿈 문자('\n', '\r')는 그대로 보존하여 원본 마크다운 파일의 라인 번호 정보를 유지함으로써,
    검출된 오류의 정확한 라인 번호를 안내할 수 있도록 합니다.

    Args:
        content (str): 검증 대상 마크다운 파일의 전체 텍스트 콘텐츠

    Returns:
        str: 코드 블록 및 인라인 코드가 공백 처리되어 정제된 마크다운 텍스트 콘텐츠
    """
    chars = list(content)
    n = len(chars)
    i = 0
    in_fenced = False
    fenced_fence = ""  # "```" 또는 "~~~"
    
    in_inline = False
    inline_backticks_count = 0
    
    while i < n:
        # 줄바꿈 문자를 만나면 인라인 코드 상태를 강제 해제 (라인 간 전파 방지)
        if chars[i] in ('\n', '\r'):
            in_inline = False
            i += 1
            continue

        if not in_inline:
            if not in_fenced:
                # 펜스드 코드 블록 시작 검사
                if i <= n - 3 and chars[i:i+3] == ['`', '`', '`']:
                    in_fenced = True
                    fenced_fence = "```"
                    chars[i] = ' '
                    chars[i+1] = ' '
                    chars[i+2] = ' '
                    i += 3
                    continue
                elif i <= n - 3 and chars[i:i+3] == ['~', '~', '~']:
                    in_fenced = True
                    fenced_fence = "~~~"
                    chars[i] = ' '
                    chars[i+1] = ' '
                    chars[i+2] = ' '
                    i += 3
                    continue
            else:
                # 펜스드 코드 블록 종료 검사
                if fenced_fence == "```" and i <= n - 3 and chars[i:i+3] == ['`', '`', '`']:
                    in_fenced = False
                    chars[i] = ' '
                    chars[i+1] = ' '
                    chars[i+2] = ' '
                    i += 3
                    continue
                elif fenced_fence == "~~~" and i <= n - 3 and chars[i:i+3] == ['~', '~', '~']:
                    in_fenced = False
                    chars[i] = ' '
                    chars[i+1] = ' '
                    chars[i+2] = ' '
                    i += 3
                    continue
        
        if in_fenced:
            # 펜스드 코드 블록 내부의 문자는 줄바꿈 문자(\n, \r)가 아니면 공백으로 대체
            if chars[i] not in ('\n', '\r'):
                chars[i] = ' '
            i += 1
            continue
            
        # 인라인 코드 (Backticks) 검사
        if not in_fenced:
            if chars[i] == '`':
                # 연속된 백틱의 개수를 셉니다.
                count = 0
                while i + count < n and chars[i + count] == '`':
                    count += 1
                
                if in_inline:
                    if count == inline_backticks_count:
                        in_inline = False
                        for c in range(count):
                            chars[i + c] = ' '
                        i += count
                        continue
                else:
                    in_inline = True
                    inline_backticks_count = count
                    for c in range(count):
                        chars[i + c] = ' '
                    i += count
                    continue
            
            if in_inline:
                if chars[i] not in ('\n', '\r'):
                    chars[i] = ' '
        
        i += 1
        
    return "".join(chars)


def verify_markdown_content(file_path: str, base_dir: str) -> List[Dict]:
    """단일 마크다운 파일의 콘텐츠 내 링크 및 비표준 이중 대괄호를 검증합니다.

    Args:
        file_path (str): 검사 대상 마크다운 파일의 절대 혹은 상대 경로
        base_dir (str): 검사를 수행하는 기본 디렉터리 경로 (상대 경로 해소 및 검증용)

    Returns:
        List[Dict]: 발견된 링크 및 린트 오류들의 목록. 각 오류는 파일 경로, 라인 번호, 
                    에러 유형, 문제가 된 경로, 에러 메시지를 포함합니다.
    """
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()
    except Exception as e:
        errors.append({
            "file": file_path,
            "line": 0,
            "type": "file_read_error",
            "path": "",
            "message": f"파일을 읽는 동안 오류가 발생했습니다: {str(e)}"
        })
        return errors

    # 코드 블록 및 인라인 코드 영역 제거로 오탐(False Positive) 방증
    cleaned_content = remove_code_elements(raw_content)
    lines = cleaned_content.splitlines()
    in_frontmatter = False

    for idx, line in enumerate(lines, 1):
        # YAML Frontmatter (문두의 --- 영역) 스킵 로직
        if idx == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() == "---":
                in_frontmatter = False
            continue

        # 1. 비표준 이중 대괄호(Double Bracket) 검출
        double_brackets = DOUBLE_BRACKET_RE.findall(line)
        if double_brackets:
            for db in double_brackets:
                errors.append({
                    "file": file_path,
                    "line": idx,
                    "type": "double_bracket",
                    "path": f"[[{db}]]",
                    "message": f"비표준 이중 대괄호가 본문 내에 잔존하고 있습니다: [[{db}]]"
                })

        # 2. 표준 마크다운 링크 파싱 및 물리 파일 존재 여부 검사
        links = LINK_RE.findall(line)
        for text, path in links:
            # URL 디코딩 처리 (공백을 나타내는 %20 등 안전 디코딩)
            unquoted_path = urllib.parse.unquote(path)

            # 앵커 부분 제거 (예: doc.md#section -> doc.md)
            clean_path = unquoted_path.split("#")[0]

            # 비어있는 경로(예: #only-anchor)는 대상에서 제외
            if not clean_path:
                continue

            # 외부 웹 링크(http, https, mailto 등)는 검사 대상에서 스킵
            if clean_path.startswith(("http://", "https://", "mailto:", "ftp:")):
                continue

            # 절대 파일 주소(file:///) 제약 조건 위반 검사
            if clean_path.startswith("file:///"):
                errors.append({
                    "file": file_path,
                    "line": idx,
                    "type": "forbidden_absolute_link",
                    "path": path,
                    "message": f"금지된 절대 파일 주소(file:///) 표기가 발견되었습니다: {path}"
                })
                continue

            # 로컬 상대 경로가 실제로 실존하는지 검사
            file_dir = os.path.dirname(file_path)
            full_target_path = os.path.join(file_dir, clean_path)

            # 물리 파일 실존 여부 파악 (os.path.exists)
            if not os.path.exists(full_target_path):
                errors.append({
                    "file": file_path,
                    "line": idx,
                    "type": "broken_link",
                    "path": path,
                    "message": f"실제 물리 파일이 존재하지 않는 데드 링크입니다: {path}"
                })

    return errors


def scan_directory(base_dir: str) -> Tuple[List[Dict], int]:
    """지정된 디렉터리 내의 모든 마크다운 파일을 재귀적으로 탐색하여 링크 검증을 수행합니다.

    Args:
        base_dir (str): 마크다운 파일을 검색하고 검증할 기본 디렉터리 경로

    Returns:
        Tuple[List[Dict], int]: (탐색된 모든 파일에서 검출된 오류 목록, 검사 완료한 총 파일 개수)
    """
    all_errors = []
    total_files = 0

    for root, dirs, files in os.walk(base_dir):
        # 불필요한 Git, 빌드 및 가상환경 캐시 디렉터리는 스캔에서 제외
        dirs[:] = [d for d in dirs if d not in (".git", ".github", ".vscode", ".pytest_cache", "__pycache__", "venv", "node_modules")]

        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                total_files += 1
                file_errors = verify_markdown_content(file_path, base_dir)
                all_errors.extend(file_errors)

    return all_errors, total_files


# =========================================================================
# SECTION 4. Command Line Interface (CLI 실행 진입점)
# =========================================================================

def main():
    """자율 링크 검증기 CLI 실행의 주 진입점입니다."""
    # 기본 검사 대상: 워크스페이스 내의 .agents 디렉터리
    workspace_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../../")
    )
    target_dir = os.path.join(workspace_root, ".agents")

    print(f"Starting Link Validator on directory: {target_dir}")

    if not os.path.exists(target_dir):
        print(f"Error: Target directory does not exist: {target_dir}")
        sys.exit(1)

    all_errors, total_files = scan_directory(target_dir)

    print("\n--- Validation Summary ---")
    print(f"Total Markdown Files Checked: {total_files}")
    print(f"Total Errors Found: {len(all_errors)}")
    print("--------------------------\n")

    if all_errors:
        print("Detailed Error Reports:")
        for idx, err in enumerate(all_errors, 1):
            # 상대 경로를 활용하여 WSL 평문 상대 경로 제약 사항을 준수하고 가독성을 확보
            relative_file = os.path.relpath(err["file"], workspace_root)
            print(
                f"{idx}. File: {relative_file}:{err['line']}\n"
                f"   Type: {err['type']}\n"
                f"   Path: {err['path']}\n"
                f"   Message: {err['message']}\n"
            )
        sys.exit(1)
    else:
        print("All link validations passed successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
