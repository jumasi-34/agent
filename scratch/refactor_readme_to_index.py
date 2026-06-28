#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess

# =========================================================================
# SECTION 1. Configurations (기본 설정 및 대상 매핑)
# =========================================================================

WORKSPACE_ROOT = "/home/jumasi/workstation"
AGENTS_DIR = os.path.join(WORKSPACE_ROOT, ".agents")

# 리팩토링 대상 디렉토리 및 매핑
# (relative_path, new_filename_base, new_id, current_readme_id)
TARGETS = [
    ("context/evals", "evals-index", "eval.index", "eval.readme"),
    ("context/guide", "guide-index", "guide.index", "guide.readme"),
    ("context/domain", "domain-index", "domain.index", "domain.readme"),
    ("context/prd", "prd-index", "prd.index", "prd.readme"),
    ("context/checklist", "checklist-index", "checklist.index", "checklist.readme"),
    ("context/infra", "infra-index", "infra.index", "infra.readme"),
    ("rules", "rules-index", "rule.index", "rule.readme"),
]

def run_git_mv(src_rel, dest_rel):
    """Git mv 명령어를 실행하여 이력을 보존하며 개명 (AGENTS_DIR 기준)"""
    src_abs = os.path.join(AGENTS_DIR, src_rel)
    if os.path.exists(src_abs):
        cmd = ["git", "mv", src_rel, dest_rel]
        print(f"Executing: {' '.join(cmd)} inside {AGENTS_DIR}")
        subprocess.run(cmd, cwd=AGENTS_DIR, check=True)
    else:
        print(f"Warning: Source file {src_abs} does not exist.")

def update_frontmatter_and_content(file_path, new_id, folder_depth):
    """개명된 인덱스 파일의 Frontmatter 및 상위 링킹 정보 수정"""
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Frontmatter ID 수정
    content = re.sub(r"^id:\s*\S+", f"id: {new_id}", content, flags=re.MULTILINE)
    
    # Frontmatter parent 수정
    content = re.sub(r"^parent:\s*\S+", "parent: concept.home", content, flags=re.MULTILINE)

    # Connections/Overview 내의 parent 링크 수정
    # Depth에 맞는 상대경로 계산
    parent_rel_path = "../" * folder_depth + "AGENTS.md"
    
    # "Parent (상위 개념)" 또는 "상위 개념" 링크 수정
    content = re.sub(
        r"(\*\s*\*?Parent \(상위 개념\)\*?:\s*)\[.*?\]\s*\(.*?\)",
        rf"\1[AGENTS.md]({parent_rel_path})",
        content
    )
    content = re.sub(
        r"(\*\s*\*?상위 개념\*?:\s*)\[.*?\]\s*\(.*?\)",
        rf"\1[AGENTS.md]({parent_rel_path})",
        content
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated index file: {file_path}")

def update_child_documents(dir_path, new_readme_filename, old_readme_id, new_readme_id):
    """개별 폴더 내 하위 문서들의 parent 필드 및 Connections 링크 수정"""
    for root, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith(".md") or file == new_readme_filename:
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # YAML Frontmatter parent 수정
            content = re.sub(
                r"^parent:\s*" + re.escape(old_readme_id),
                f"parent: {new_readme_id}",
                content,
                flags=re.MULTILINE
            )

            # README.md 링크를 신규 인덱스 파일명으로 보정
            content = re.sub(
                r"README\.md",
                new_readme_filename,
                content
            )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Updated child document: {file}")

def update_global_agents_file():
    """최상위 AGENTS.md 파일 내의 7대 도메인 링킹 정보 수정"""
    agents_file_path = os.path.join(AGENTS_DIR, "AGENTS.md")
    if not os.path.exists(agents_file_path):
        print("AGENTS.md not found!")
        return

    with open(agents_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # README.md 링크들을 각각 매핑된 *-index.md 명칭으로 정밀 보정
    for rel_path, new_filename_base, _, _ in TARGETS:
        old_pattern = f"{rel_path}/README.md"
        new_replacement = f"{rel_path}/{new_filename_base}.md"
        content = content.replace(old_pattern, new_replacement)

    with open(agents_file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated AGENTS.md globally.")

def main():
    print("Starting Domain Gateway Refactoring...")
    
    # 1. git mv 및 인덱스 파일 자체 수정, 하위 문서 수정
    for rel_path, new_filename_base, new_id, old_id in TARGETS:
        full_dir = os.path.join(AGENTS_DIR, rel_path)
        old_readme = os.path.join(full_dir, "README.md")
        new_readme_name = f"{new_filename_base}.md"
        new_readme_path = os.path.join(full_dir, new_readme_name)
        
        # 폴더 깊이 계산 (.agents/ 기준)
        # rel_path가 context/evals 면 depth는 2 (context, evals)
        # rules 면 depth는 1 (rules)
        depth = len(rel_path.split("/"))
        
        old_readme_rel = os.path.join(rel_path, "README.md")
        new_readme_rel = os.path.join(rel_path, new_readme_name)

        print(f"\nProcessing domain: {rel_path}")
        run_git_mv(old_readme_rel, new_readme_rel)
        update_frontmatter_and_content(new_readme_path, new_id, depth)
        update_child_documents(full_dir, new_readme_name, old_id, new_id)

    # 2. 최상위 AGENTS.md 전체 업데이트
    print("\nUpdating global gatekeeper AGENTS.md...")
    update_global_agents_file()

    print("\nRefactoring Completed Successfully.")

if __name__ == "__main__":
    main()
