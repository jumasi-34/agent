#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refactor_writing_short_links.py - writing 하위 폴더 단어 중복(writing-접두사) 제거에 따른 링크 갱신 스크립트
"""

import os
import re

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content

    # 1. skills/writing/writing-plans/... -> skills/writing/plans/...
    content = content.replace('skills/writing/writing-plans', 'skills/writing/plans')
    # 2. skills/writing/writing-skills/... -> skills/writing/skills/...
    content = content.replace('skills/writing/writing-skills', 'skills/writing/skills')
    # 3. skills/writing/writing-wiki/... -> skills/writing/wiki/...
    content = content.replace('skills/writing/writing-wiki', 'skills/writing/wiki')

    # index.md 및 skill-map.md의 writing-plans, writing-skills 참조 텍스트(라벨 및 주소)도 추가 보정
    # [writing-plans](.agents/skills/writing/writing-plans/SKILL.md) -> [writing-plans](.agents/skills/writing/plans/SKILL.md)
    # [writing-skills](.agents/skills/writing/writing-skills/SKILL.md) -> [writing-skills](.agents/skills/writing/skills/SKILL.md)
    # index.md 등에서의 id 및 frontmatter/related 도 갱신
    content = content.replace('id: skill.writing-plans', 'id: skill.writing.plans')
    content = content.replace('id: skill.writing-skills', 'id: skill.writing.skills')
    content = content.replace('id: skill.writing-wiki', 'id: skill.writing.wiki')

    content = content.replace('writing-plans/plan-document-reviewer-prompt', 'plans/plan-document-reviewer-prompt')
    content = content.replace('writing-skills/anthropic-best-practices', 'skills/anthropic-best-practices')
    content = content.replace('writing-skills/examples/CLAUDE_MD_TESTING', 'skills/examples/CLAUDE_MD_TESTING')
    content = content.replace('writing-skills/persuasion-principles', 'skills/persuasion-principles')
    content = content.replace('writing-skills/testing-skills-with-subagents', 'skills/testing-skills-with-subagents')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] {filepath}")

def main():
    root_dir = "/home/jumasi/workstation/.agents"
    
    # 갱신 대상 파일 리스트
    targets = [
        "agents/skill-map.md",
        "indexes/Skill Index.md",
        "skills/brainstorming/SKILL.md",
        "skills/executing-plans/SKILL.md",
        "skills/index.md",
        "skills/subagent-driven-development/SKILL.md",
        "skills/writing/plans/SKILL.md",
        "skills/writing/plans/plan-document-reviewer-prompt.md",
        "skills/writing/skills/SKILL.md",
        "skills/writing/skills/anthropic-best-practices.md",
        "skills/writing/skills/examples/CLAUDE_MD_TESTING.md",
        "skills/writing/skills/persuasion-principles.md",
        "skills/writing/skills/testing-skills-with-subagents.md",
        "skills/writing/wiki/SKILL.md",
    ]

    for rel_path in targets:
        abs_path = os.path.join(root_dir, rel_path)
        if os.path.exists(abs_path):
            replace_in_file(abs_path)
        else:
            print(f"[NOT FOUND] {abs_path}")

if __name__ == '__main__':
    main()
