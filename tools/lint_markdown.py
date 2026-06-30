#!/usr/bin/env python3
# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import os
import sys
import re
import subprocess
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# =========================================================================
# SECTION 2. Constants & Configurations (상수 및 전역 설정)
# =========================================================================
# 터미널 출력 컬러 정의 (이모지 전면 금지 규칙에 따라 기호와 텍스트로만 강조)
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

# 린트 검사 필수 5대 키
REQUIRED_FIELDS = ["id", "title", "type", "status", "updated"]

# 메타데이터 허용 규격 정의
ALLOWED_TYPES = ["rule", "wiki", "raw", "index", "principle", "reference", "skill", "agent"]
ALLOWED_STATUS = ["active", "unresolved", "resolved", "synthesized", "deprecated"]

# =========================================================================
# SECTION 3. Core Logic - Git Analyzer (Git 변경 이력 추적 및 분석)
# =========================================================================
def get_git_changes() -> Tuple[List[str], List[str]]:
    """현재 세션에서 변경(staged/unstaged)되거나 추가된 파일 목록을 추적합니다.

    메인 리포지토리와 .agents 독립 리포지토리의 변경을 통합 스캔합니다.

    Returns:
        Tuple[List[str], List[str]]: (마크다운 파일 목록, 소스 코드 파일 목록)
    """
    markdown_files = []
    code_files = []
    
    # 스캔할 대상 리포지토리 목록 (로컬 상대 경로, 결과 파일 경로에 붙일 접두사)
    target_repos = [
        (".", ""),
        (".agents", ".agents")
    ]
    
    for repo_path, prefix in target_repos:
        if not os.path.exists(repo_path):
            continue
            
        try:
            # git status --porcelain -u 명령으로 Untracked 디렉터리 내 개별 파일까지 전부 전개하여 변경 취득
            result = subprocess.run(
                ["git", "-C", repo_path, "status", "--porcelain", "-u"],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                    
                # 포맷: XY filepath (예: M app.py, ?? tests/test.py)
                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    continue
                    
                status_code, filepath = parts[0], parts[1]
                
                # 리네임 등의 포맷 대응 (예: R "old.py" -> "new.py")
                if " -> " in filepath:
                    filepath = filepath.split(" -> ")[-1].strip('"')
                else:
                    filepath = filepath.strip('"')
                    
                # 삭제된 파일은 검사에서 제외
                if status_code in ["D", "RD"]:
                    continue
                    
                # 접두사를 적용하여 최종 정규 상대 경로 획득
                if prefix:
                    final_path = os.path.join(prefix, filepath)
                else:
                    final_path = filepath
                    
                normalized_path = final_path.replace("\\", "/")
                
                # .pyc 등 캐시 파일 제거
                if "__pycache__" in normalized_path or normalized_path.endswith(".pyc"):
                    continue
                    
                if normalized_path.endswith(".md"):
                    markdown_files.append(final_path)
                elif normalized_path.endswith((".py", ".sql", ".sh")):
                    # 임시 scratch 스크립트는 지식 보강 추적 대상에서 배제
                    if not normalized_path.startswith(("scratch/", ".agent-storage/scratch/")):
                        code_files.append(final_path)
                        
        except Exception as e:
            print(f"{COLOR_YELLOW}[WARN] Git {repo_path} 리포지토리 상태 조회 실패: {str(e)}{COLOR_RESET}")
            
    return markdown_files, code_files


# =========================================================================
# SECTION 4. Core Logic - Markdown Linter & Auto-Fixer (마크다운 검증 및 교정)
# =========================================================================
def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, str]], str, int, int]:
    """마크다운 본문에서 YAML Frontmatter를 추출하고 파싱합니다.

    파이썬 표준 라이브러리만을 활용하여 이식성과 견고함을 확보합니다.

    Args:
        content (str): 마크다운 파일의 전체 텍스트 내용

    Returns:
        Tuple[Optional[Dict[str, str]], str, int, int]:
            (파싱된 딕셔너리, 본문 내용, Frontmatter 시작 라인인덱스, 끝 라인인덱스)
    """
    # 최상단 YAML Frontmatter 검색을 위한 정규식 (줄바꿈 포함)
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not fm_match:
        return None, content, -1, -1
        
    fm_text = fm_match.group(1)
    body_text = content[fm_match.end():]
    
    # 가벼운 Key-Value 파서 구현 (표준 yaml 의존성 최소화)
    metadata = {}
    lines = fm_text.splitlines()
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Key: Value 파싱
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            
            # 따옴표 제거 및 리스트 브래킷 소거
            val = val.strip('"\'')
            if val.startswith(">"):
                # Multi-line string 등의 기호는 제외
                val = val.lstrip(">").strip()
            metadata[key] = val
            
    # 전체 파일 내에서 Frontmatter의 시작 줄과 끝 줄 파악 (1-based index)
    fm_lines_count = len(fm_text.splitlines())
    return metadata, body_text, 1, fm_lines_count + 2

def suggest_metadata_defaults(filepath: str, content: str) -> Dict[str, str]:
    """지정된 파일의 속성에 맞춰 적합한 기본 메타데이터 속성을 추론하여 제공합니다.

    Args:
        filepath (str): 대상 마크다운 파일 상대 경로
        content (str): 마크다운 파일 본문 내용

    Returns:
        Dict[str, str]: 추론된 메타데이터 딕셔너리
    """
    basename = os.path.basename(filepath)
    name_no_ext = os.path.splitext(basename)[0]
    
    # 1. ID 추론
    sub_domain = "wiki"
    if "rules/" in filepath or "L1-" in basename or "L2-" in basename or "L3-" in basename:
        sub_domain = "rule"
    elif "principles/" in filepath:
        sub_domain = "principle"
    elif "raw/" in filepath:
        sub_domain = "raw"
    elif "indexes/" in filepath or "index.md" in basename:
        sub_domain = "index"
        
    inferred_id = f"{sub_domain}.{name_no_ext.replace('-', '_').lower()}"
    
    # 2. Title 추론 (파일 내 첫 # 제목 탐색)
    inferred_title = name_no_ext.replace("-", " ").replace("_", " ").title()
    title_match = re.search(r"^#\s+(.*?)$", content, re.MULTILINE)
    if title_match:
        inferred_title = title_match.group(1).strip()
        # 대괄호 장식 보정 (예: [Rule] 등 접두사가 없다면 붙여줌)
        if sub_domain == "rule" and not inferred_title.startswith("[Rule]"):
            inferred_title = f"[Rule] {inferred_title}"
        elif sub_domain == "wiki" and not inferred_title.startswith("[Wiki]"):
            inferred_title = f"[Wiki] {inferred_title}"
            
    # 3. Type 추론
    inferred_type = sub_domain
    if inferred_type not in ALLOWED_TYPES:
        inferred_type = "wiki"
        
    # 4. Status 추론
    inferred_status = "active"
    if sub_domain == "raw":
        inferred_status = "unresolved"
        
    return {
        "id": inferred_id,
        "title": inferred_title,
        "type": inferred_type,
        "status": inferred_status,
        "updated": datetime.today().strftime("%Y-%m-%d")
    }

def lint_and_fix_markdown(filepath: str) -> Tuple[bool, List[str]]:
    """단일 마크다운 파일의 Frontmatter를 검사하고 미비점을 자율 교정(Auto-Fix)합니다.

    Args:
        filepath (str): 대상 파일 경로

    Returns:
        Tuple[bool, List[str]]: (수정/보정 실행 여부, 검출된 경고/안내 메시지 리스트)
    """
    warnings = []
    fixed = False
    
    if not os.path.exists(filepath):
        return False, [f"파일이 존재하지 않습니다: {filepath}"]
        
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        
    metadata, body, start_ln, end_ln = parse_frontmatter(content)
    defaults = suggest_metadata_defaults(filepath, content)
    
    # Frontmatter가 완전히 누락된 경우 새로 빌드하여 맨 위에 강제 삽입
    if metadata is None:
        warnings.append("YAML Frontmatter 헤더가 완전히 누락되어 신규 템플릿을 빌드 및 삽입합니다.")
        new_fm = f"""---
id: {defaults['id']}
title: "{defaults['title']}"
type: {defaults['type']}
status: {defaults['status']}
summary: >
  본 문서는 이 세션에서 생성/수정된 {defaults['title']} 자산입니다.
updated: {defaults['updated']}
---

"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_fm + content.lstrip())
        return True, warnings
        
    # 필수 필드 유실 여부 검증 및 교정
    updated_metadata = metadata.copy()
    meta_changed = False
    
    for field in REQUIRED_FIELDS:
        if field not in metadata or not metadata[field].strip():
            warnings.append(f"필수 메타데이터 필드 '{field}'가 유실되어 자동 보정값을 할당합니다.")
            updated_metadata[field] = defaults[field]
            meta_changed = True
            
    # 허용 규격 외의 데이터 분류 검증 및 자동 보정
    if updated_metadata.get("type") not in ALLOWED_TYPES:
        warnings.append(f"허용되지 않은 type 값 '{updated_metadata.get('type')}'을 자동 기본값 '{defaults['type']}'으로 리셋합니다.")
        updated_metadata["type"] = defaults["type"]
        meta_changed = True
        
    if updated_metadata.get("status") not in ALLOWED_STATUS:
        warnings.append(f"허용되지 않은 status 값 '{updated_metadata.get('status')}'을 자동 기본값 '{defaults['status']}'으로 리셋합니다.")
        updated_metadata["status"] = defaults["status"]
        meta_changed = True
        
    # 날짜 포맷 검사 및 강제 최신화
    date_str = updated_metadata.get("updated", "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        warnings.append(f"올바르지 않은 날짜 형식 '{date_str}'을 현재 일자 '{defaults['updated']}'로 교정합니다.")
        updated_metadata["updated"] = defaults["updated"]
        meta_changed = True
        
    # 변경 사항이 있는 경우 Frontmatter 블록만 정밀 리빌드하여 병합 (본문 주석 및 데이터 보존)
    if meta_changed:
        # 기존 Frontmatter 라인 분석 및 값 교체 방식 적용 (주석과 다른 비필수 메타 필드 보존을 위함)
        raw_lines = content.splitlines()
        fm_block_lines = raw_lines[start_ln:end_ln-1]
        
        rebuilt_fm_lines = []
        applied_fields = set()
        
        for line in fm_block_lines:
            stripped = line.strip()
            if ":" in stripped and not stripped.startswith("#"):
                key, _ = stripped.split(":", 1)
                key = key.strip()
                if key in REQUIRED_FIELDS:
                    # 보정된 새 값으로 교체하여 삽입
                    val = updated_metadata[key]
                    if " " in val or "[" in val or "]" in val or ":" in val:
                        rebuilt_fm_lines.append(f"{key}: \"{val}\"")
                    else:
                        rebuilt_fm_lines.append(f"{key}: {val}")
                    applied_fields.add(key)
                    continue
            rebuilt_fm_lines.append(line)
            
        # 혹시나 원본 Frontmatter에 누락되었던 필수 필드가 있다면 마저 추가
        for field in REQUIRED_FIELDS:
            if field not in applied_fields:
                val = updated_metadata[field]
                if " " in val or "[" in val or "]" in val or ":" in val:
                    rebuilt_fm_lines.append(f"{field}: \"{val}\"")
                else:
                    rebuilt_fm_lines.append(f"{field}: {val}")
                    
        # 새 콘텐츠 조합
        new_content = "---\n" + "\n".join(rebuilt_fm_lines) + "\n---\n" + body
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixed = True
        
    return fixed, warnings

# =========================================================================
# SECTION 5. Verification Gate (지식 결핍 감지 및 통합 무결성 보증)
# =========================================================================
def check_knowledge_sync(markdown_changed: List[str], code_changed: List[str]) -> bool:
    """소스 코드 수정에 수반되는 지식 갱신(Wiki/Index 추가 및 보강) 누락 여부를 확인합니다.

    Args:
        markdown_changed (List[str]): 변경된 마크다운 파일들
        code_changed (List[str]): 변경된 소스 코드 파일들

    Returns:
        bool: 지식이 정상적으로 갱신되었거나 검사 대상이 아니면 True, 누락 결핍 상태면 False
    """
    if not code_changed:
        # 소스 코드 변경이 없으면 무조건 통과
        return True
        
    # 변경된 마크다운 중 실제 지식 자산 폴더(.agents/wiki/ 또는 .agents/indexes/ 등)에 속하는 파일이 있는지 체크
    knowledge_updated = False
    for md_file in markdown_changed:
        normalized = md_file.replace("\\", "/")
        if ".agents/wiki/" in normalized or ".agents/indexes/" in normalized or normalized.endswith("index.md"):
            knowledge_updated = True
            break
            
    if not knowledge_updated:
        print(f"\n{COLOR_RED}{COLOR_BOLD}[KNOWLEDGE_OUT_OF_SYNC] 소스 코드 변경에 따른 지식 동기화 누락 경고!{COLOR_RESET}")
        print(f"{COLOR_YELLOW}수정된 프로덕션 코드 파일:{COLOR_RESET}")
        for code_file in code_changed:
            print(f"  - {code_file}")
            
        print(f"\n{COLOR_BOLD}권장 사항 (안드레 카파시의 지식 큐레이션 수칙):{COLOR_RESET}")
        print("  - 소스 코드를 생성하거나 리팩토링한 경우, 해당 로직과 설계 방향성을 반드시 아카이빙해야 합니다.")
        print("  - [수행 가이드]: `.agents/wiki/` 하위에 관련 설계 및 분석을 담은 Wiki 문서를 작성/갱신하거나,")
        print("    혹은 `.agents/indexes/` 하위 인덱스 문서를 최신 상태로 갱신하여 인지 무결성을 유지해 주십시오.")
        print("  - 지식 보강 완료 후 다시 본 린트 스크립트를 기동하십시오.\n")
        return False
        
    return True

# =========================================================================
# SECTION 6. Main Execution (프로그램 메인 진입점)
# =========================================================================
def main():
    print(f"{COLOR_BLUE}{COLOR_BOLD}===================================================={COLOR_RESET}")
    print(f"{COLOR_BLUE}{COLOR_BOLD}       KNOWLEDGE METADATA LINTER & CURATOR          {COLOR_RESET}")
    print(f"{COLOR_BLUE}{COLOR_BOLD}===================================================={COLOR_RESET}")
    
    # 1. 인자 분석 및 대상 파일 수집
    markdown_changed = []
    code_changed = []
    all_scan_mode = False
    
    # 스캔 대상 수동 지정 판단 (--all 또는 특정 파일/디렉터리 경로)
    targets = sys.argv[1:]
    if targets:
        all_scan_mode = True
        print(f" 수동 정밀 검사 및 리팩토링 모드 활성화 (대상: {targets})")
        
        # 특정 파일이나 디렉터리를 재귀적으로 스캔
        for target in targets:
            if target == "--all":
                # 워크스페이스 내 전체 .md 파일 스캔 (임시/제외 디렉터리 제외)
                search_dirs = [".agents", "docs", "intelligence"]
                for sd in search_dirs:
                    if os.path.exists(sd):
                        for root, dirs, files in os.walk(sd):
                            # 캐시 및 임시 폴더 건너뜀
                            dirs[:] = [d for d in dirs if d not in ["__pycache__", ".git", ".github", "temp", "trash"]]
                            for file in files:
                                if file.endswith(".md"):
                                    markdown_changed.append(os.path.join(root, file))
            elif os.path.isdir(target):
                for root, dirs, files in os.walk(target):
                    dirs[:] = [d for d in dirs if d not in ["__pycache__", ".git", ".github", "temp", "trash"]]
                    for file in files:
                        if file.endswith(".md"):
                            markdown_changed.append(os.path.join(root, file))
            elif os.path.isfile(target) and target.endswith(".md"):
                markdown_changed.append(target)
                
        markdown_changed = sorted(list(set(markdown_changed)))
    else:
        # 기존: Git 변경 사항 스캔
        print(" Git Status 변경 세션 스캔 중...")
        markdown_changed, code_changed = get_git_changes()
        
    if not markdown_changed and not code_changed:
        print(f"{COLOR_GREEN}✔ 정상: 검사 및 수정할 수 있는 대상 마크다운 파일이 발견되지 않았습니다.{COLOR_RESET}\n")
        sys.exit(0)
        
    print(f"  └ 검사 대상 마크다운 파일: {len(markdown_changed)}개")
    if not all_scan_mode:
        print(f"  └ 변경된 소스코드 파일: {len(code_changed)}개")
    
    # 2. 각 마크다운 파일 린트 및 Auto-Fix 수행
    lint_failed = False
    fixed_count = 0
    
    if markdown_changed:
        print("\n 마크다운 메타데이터(Frontmatter) 검증 및 자동 보정 시작...")
        for md_file in markdown_changed:
            try:
                fixed, warnings = lint_and_fix_markdown(md_file)
                if warnings:
                    print(f"\n[{md_file}] 검출 사항:")
                    for w in warnings:
                        print(f"  - {COLOR_YELLOW}{w}{COLOR_RESET}")
                        
                if fixed:
                    fixed_count += 1
                    print(f"[{md_file}] -> {COLOR_GREEN}✔ 자동 보정(Auto-Fix) 완료!{COLOR_RESET}")
                else:
                    # 전수 정밀 모드에서는 출력이 너무 길어질 수 있으므로, 무결함 파일은 한 줄 요약 혹은 생략 가능하나 일단 로그 표시
                    print(f"[{md_file}] -> {COLOR_GREEN}✔ 무결함 (통과){COLOR_RESET}")
            except Exception as e:
                print(f"[{md_file}] -> {COLOR_RED}✘ 에러 발생: {str(e)}{COLOR_RESET}")
                lint_failed = True
                
    # 3. 지식 갱신(결핍 여부) 정밀 감사 (수동 전체 스캔 모드에서는 지식 결핍 감지 제외)
    sync_passed = True
    if not all_scan_mode:
        print("\n 소스 코드 수정 대비 지식 동기화 정밀 검사 진행...")
        sync_passed = check_knowledge_sync(markdown_changed, code_changed)
    
    # 4. 종합 최종 판정 및 종료 코드 매핑
    print(f"\n{COLOR_BLUE}{COLOR_BOLD}===================================================={COLOR_RESET}")
    print(f"{COLOR_BLUE}{COLOR_BOLD}                  최종 분석 리포트                    {COLOR_RESET}")
    print(f"{COLOR_BLUE}{COLOR_BOLD}===================================================={COLOR_RESET}")
    
    if lint_failed:
        print(f"{COLOR_RED}✘ 빌드 차단: 마크다운 파싱 도중 심각한 구문 에러가 발견되었습니다.{COLOR_RESET}\n")
        sys.exit(1)
        
    if not sync_passed:
        print(f"{COLOR_YELLOW}[WARN] 지식 결핍 경고: 소스 코드가 고쳐졌으나 Wiki/Index 지식이 동기화되지 않았습니다.{COLOR_RESET}")
        print(f"{COLOR_YELLOW}에이전트는 Wiki/Index를 보강한 후에 작업을 종료할 것을 강하게 권장합니다.{COLOR_RESET}\n")
        # 경고 상태(KNOWLEDGE_OUT_OF_SYNC)를 알리는 독립 종료코드 2 리턴
        sys.exit(2)
        
    print(f"{COLOR_GREEN}{COLOR_BOLD}✔ 모든 마크다운 메타데이터 표준 충족 및 지식 동기화가 완벽합니다!{COLOR_RESET}")
    if fixed_count > 0:
        print(f"  └ 총 {fixed_count}개의 마크다운 파일이 메타데이터 표준 규격으로 자동 보정되었습니다.")
    print("")
    sys.exit(0)

if __name__ == "__main__":
    main()
