# * [Wiki - 정적 정합성 검사 링터 스크립트]
"""Wiki 정적 정합성 검사 링터 모듈.

이 모듈은 .agents 디렉터리 하위의 wiki, indexes, rules 디렉터리에 존재하는
모든 마크다운 파일들을 분석하여 깨진 상대 경로 링크 및 고립된 페이지를 검출합니다.
"""

# =========================================================================
# SECTION 1. Imports (라이브러리 및 모듈 임포트)
# =========================================================================
import os
import re
from pathlib import Path
from typing import List, Dict, Set

# =========================================================================
# SECTION 2. Constants & Path Config (상수 및 경로 설정)
# =========================================================================
WORKSPACE_ROOT = Path("/home/jumasi/workstation")
AGENTS_DIR = WORKSPACE_ROOT / ".agents"
WIKI_DIR = AGENTS_DIR / "wiki"
INDEXES_DIR = AGENTS_DIR / "indexes"
RULES_DIR = AGENTS_DIR / "rules"

# =========================================================================
# SECTION 3. Lint Engine (정적 분석 핵심 기능부)
# =========================================================================

def get_markdown_files(directory: Path) -> List[Path]:
    """지정한 디렉터리 하위의 모든 마크다운(.md) 파일을 재귀적으로 검색합니다.

    Args:
        directory (Path): 탐색할 기준 디렉터리 경로.

    Returns:
        List[Path]: 검색된 마크다운 파일들의 Path 객체 리스트.
    """
    if not directory.exists():
        return []
    return list(directory.glob("**/*.md"))


def extract_links(file_path: Path) -> List[str]:
    """마크다운 파일 본문에서 외부 링크를 제외한 상대 경로 링크 패턴을 추출합니다.

    Args:
        file_path (Path): 분석 대상 마크다운 파일 경로.

    Returns:
        List[str]: 상대 경로 링크 목록 (앵커 링크 구분값 `#`은 제거됨).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except IOError:
        return []
        
    # [link text](relative_path) 패턴 중 외부 주소(http, https, file 등)가 아닌 상대 경로만 추출
    links = re.findall(r"\[.*?\]\((?!http|https|file)(.*?)\)", content)
    # 앵커(#)를 포함하는 경우 파일 경로 부분만 분리하여 리턴
    return [link.split("#")[0] for link in links if link]


def run_wiki_lint() -> Dict[str, List[str]]:
    """Wiki 영역 내에 존재하는 깨진 링크 및 고립된 페이지를 전수 진단합니다.

    Returns:
        Dict[str, List[str]]: 'broken_links' 및 'orphan_pages' 오류 메시지 목록을 담은 딕셔너리.
    """
    issues: Dict[str, List[str]] = {
        "broken_links": [],
        "orphan_pages": []
    }
    
    all_wiki_files = get_markdown_files(WIKI_DIR)
    all_index_files = get_markdown_files(INDEXES_DIR)
    all_rule_files = get_markdown_files(RULES_DIR)
    
    all_monitored_files = all_wiki_files + all_index_files + all_rule_files
    
    # 정합성을 모니터링할 파일들의 워크스페이스 기준 상대 경로 목록 빌드
    monitored_paths_set: Set[str] = {
        os.path.relpath(p, WORKSPACE_ROOT) for p in all_monitored_files
    }
    
    referenced_paths: Set[str] = set()
    
    # 1. 깨진 상대 경로 링크 검출 및 참조 관계 맵 수집
    for file_path in all_monitored_files:
        rel_src = os.path.relpath(file_path, WORKSPACE_ROOT)
        links = extract_links(file_path)
        
        for link in links:
            # 앵커 주소나 비어 있는 링크 제외
            if not link.strip():
                continue
                
            # 워크스페이스 루트 기준 상대 경로 또는 파일 기준 상대 경로 판별
            if link.startswith((".agents", "app", "tests", "data", "static", "docs", "logs")):
                target_path = (WORKSPACE_ROOT / link).resolve()
            else:
                src_dir = file_path.parent
                target_path = (src_dir / link).resolve()
            
            if not target_path.exists():
                issues["broken_links"].append(
                    f"{rel_src} 파일 내 존재하지 않는 파일 링크 발견: {link}"
                )
            else:
                rel_target = os.path.relpath(target_path, WORKSPACE_ROOT)
                referenced_paths.add(rel_target)
                
    # 2. 고립된 Wiki 페이지(어느 인덱스나 다른 위키에서도 링크하지 않는 문서) 검출
    for wiki_file in all_wiki_files:
        rel_wiki = os.path.relpath(wiki_file, WORKSPACE_ROOT)
        if rel_wiki not in referenced_paths:
            issues["orphan_pages"].append(
                f"고립된 Wiki 문서 (어떤 지식이나 인덱스도 링크하지 않음): {rel_wiki}"
            )
            
    return issues


# =========================================================================
# SECTION 4. Execution Entrypoint (프로그램 엔트리포인트)
# =========================================================================
if __name__ == "__main__":
    print("[Wiki Lint] 검사를 시작합니다...")
    results = run_wiki_lint()
    
    has_issues = False
    if results["broken_links"]:
        has_issues = True
        print("\n[오류] 존재하지 않는 상대 경로 링크가 감지되었습니다:")
        for err in results["broken_links"]:
            print(f" - {err}")
            
    if results["orphan_pages"]:
        has_issues = True
        print("\n[경고] 다른 문서에 의해 연결되지 않은 고립된 Wiki 파일이 존재합니다:")
        for wrn in results["orphan_pages"]:
            print(f" - {wrn}")
            
    if not has_issues:
        print("\n[성공] 모든 Wiki 링크 및 인덱스 정합성 검사를 무결하게 통과하였습니다.")
