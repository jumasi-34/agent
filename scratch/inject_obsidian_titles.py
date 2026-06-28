#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inject_obsidian_titles.py - 모든 SKILL.md 및 하위 .md 자산들에 대해,
폴더 경로명과 기존 Frontmatter name을 분석하여 식별하기 매우 명확한 고유 'title'을
Frontmatter 내에 자동으로 주입/갱신해 주는 똑똑한 스크립트.
"""

import os
import re

def build_unique_title(filepath, root_dir):
    # 상대 경로 획득 (예: skills/writing/plans/SKILL.md)
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    parts = rel_path.split('/')
    
    # 1. 스킬 문서인 경우 (SKILL.md)
    if parts[-1].upper() == "SKILL.MD":
        if len(parts) >= 3:
            category = parts[-2].upper() # plans, tdd 등
            parent_cat = parts[-3].upper() # writing, quality 등
            return f"Skill: {parent_cat} > {category}"
        elif len(parts) == 2:
            category = parts[-2].upper()
            return f"Skill: {category}"
        return "Skill: Core Instruction"
    
    # 2. 일반 마크다운 가이드 문서인 경우 (예: references/agents.md)
    filename = os.path.splitext(parts[-1])[0].upper()
    if len(parts) >= 3:
        parent_folder = parts[-2].upper()
        grandparent_folder = parts[-3].upper()
        return f"Ref: {grandparent_folder} > {parent_folder} > {filename}"
    elif len(parts) == 2:
        parent_folder = parts[-2].upper()
        return f"Ref: {parent_folder} > {filename}"
    
    return f"Ref: {filename}"

def inject_title_to_yaml(filepath, root_dir):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Frontmatter가 존재하는지 확인 (--- 로 감싸진 영역)
    if not content.startswith('---'):
        return

    end_idx = content.find('---', 3)
    if end_idx == -1:
        return

    frontmatter = content[3:end_idx]
    body = content[end_idx:]

    # 기존에 title이 있는지 파싱
    title_pattern = re.compile(r'^title:\s*(.*)$', re.MULTILINE)
    match = title_pattern.search(frontmatter)

    unique_title = build_unique_title(filepath, root_dir)

    if match:
        # 이미 존재하더라도 더 유니크한 조합명으로 갱신
        old_title_line = match.group(0)
        new_title_line = f'title: "{unique_title}"'
        new_frontmatter = frontmatter.replace(old_title_line, new_title_line)
    else:
        # 존재하지 않으면 추가 (대개 id: 밑단 또는 첫 줄에 삽입)
        # id 속성 아래에 주입해 가시성을 지킴
        id_match = re.search(r'^(id:\s*.*)$', frontmatter, re.MULTILINE)
        if id_match:
            new_frontmatter = frontmatter.replace(id_match.group(0), f'{id_match.group(0)}\ntitle: "{unique_title}"')
        else:
            new_frontmatter = f'title: "{unique_title}"\n' + frontmatter

    if frontmatter != new_frontmatter:
        new_content = '---' + new_frontmatter + body
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"[TITLE INJECTED] {filepath} -> title: \"{unique_title}\"")

def main():
    root_dir = "/home/jumasi/workstation/.agents"
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in {".git", ".github", "scratch", "node_modules", ".venv", "__pycache__"}]
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                inject_title_to_yaml(filepath, root_dir)

if __name__ == '__main__':
    main()
