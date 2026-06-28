#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_obsidian_extension_links.py - 모든 .md 파일 본문 내의 [[skills/...]] 혹은 [[...]] 위키 링크 중,
참조하는 물리 대상이 .md 파일임에도 불구하고 확장자가 누락된 링크들을 전수 탐색하여
[[.../filename.md]] 형태로 물리 확장자를 확실히 일원화하여 붙여주는 무결성 보정 스크립트.
"""

import os
import re

# 정규식: [[ ... ]] 패턴 추출
WIKI_LINK_PATTERN = re.compile(r'(\[\[([^\]]+)\]\])')

def process_file(filepath, root_dir):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    modified = False

    # 문서 내의 모든 [[ ... ]] 링크 분석
    matches = WIKI_LINK_PATTERN.findall(content)
    for full_match, link_path in matches:
        # 이미 확장자가 지정되었거나 파이프(|) 기호, 혹은 SKILL, AGENTS 등의 특수 명칭은 통과
        if '.' in link_path or '|' in link_path:
            continue
        
        # Obsidian Vault 내 상대 경로인지 확인
        # 링크 주소가 skills/... 등으로 구성된 경우
        # 실제 워크스페이스 상에서 매칭되는 파일이 존재하는지 검증
        potential_rel_path = link_path.strip()
        
        # 1. .md를 붙여서 실제 파일이 존재하면 변경
        test_file_path = os.path.join(root_dir, potential_rel_path + ".md")
        if os.path.exists(test_file_path):
            old_link = f"[[{link_path}]]"
            new_link = f"[[{potential_rel_path}.md]]"
            content = content.replace(old_link, new_link)
            modified = True
            print(f"  - {filepath}: {old_link} -> {new_link}")

    if modified and content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIXED EXTENSION] {filepath}")

def main():
    root_dir = "/home/jumasi/workstation/.agents"
    
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in {".git", ".github", "scratch", "node_modules", ".venv", "__pycache__"}]
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                process_file(filepath, root_dir)

if __name__ == '__main__':
    main()
