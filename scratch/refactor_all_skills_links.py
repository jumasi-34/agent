#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refactor_all_skills_links.py - .agents 전체 구조에 걸친 스킬 폴더 일괄 마이그레이션에 대응하는 링크/메타 수정 스크립트
"""

import os
import re

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content

    # 1. collaboration 범주
    content = content.replace('skills/dispatching-parallel-agents', 'skills/collaboration/parallel-agents')
    content = content.replace('skills/subagent-driven-development', 'skills/collaboration/subagent-development')
    content = content.replace('skills/executing-plans', 'skills/collaboration/execute-plans')
    content = content.replace('skills/handoff', 'skills/collaboration/handoff')

    # 2. memory 범주
    content = content.replace('skills/agentmemory', 'skills/memory/core')
    content = content.replace('skills/remember', 'skills/memory/remember')
    content = content.replace('skills/recall', 'skills/memory/recall')
    content = content.replace('skills/forget', 'skills/memory/forget')
    content = content.replace('skills/recap', 'skills/memory/recap')
    content = content.replace('skills/session-history', 'skills/memory/session-history')
    content = content.replace('skills/commit-history', 'skills/memory/commit-history')
    content = content.replace('skills/commit-context', 'skills/memory/commit-context')

    # 3. quality 범주
    content = content.replace('skills/guardrail', 'skills/quality/guardrail')
    content = content.replace('skills/sql_analyzer', 'skills/quality/sql')
    content = content.replace('skills/korean_metadata', 'skills/quality/korean-metadata')
    content = content.replace('skills/receiving-code-review', 'skills/quality/receive-review')
    content = content.replace('skills/requesting-code-review', 'skills/quality/request-review')
    content = content.replace('skills/verification-before-completion', 'skills/quality/verify-completion')

    # 4. development 범주
    content = content.replace('skills/developing-with-streamlit', 'skills/development/streamlit')
    content = content.replace('skills/frontend-design', 'skills/development/design')
    content = content.replace('skills/test-driven-development', 'skills/development/tdd')
    content = content.replace('skills/using-git-worktrees', 'skills/development/worktrees')
    content = content.replace('skills/systematic-debugging', 'skills/development/debugging')

    # Frontmatter ID 및 텍스트 갱신들 (필요한 경우)
    content = content.replace('id: skill.dispatching_parallel_agents', 'id: skill.collaboration.parallel_agents')
    content = content.replace('id: skill.subagent_driven_development', 'id: skill.collaboration.subagent_development')
    content = content.replace('id: skill.executing_plans', 'id: skill.collaboration.execute_plans')
    content = content.replace('id: skill.handoff', 'id: skill.collaboration.handoff')

    content = content.replace('id: skill.agentmemory', 'id: skill.memory.core')
    content = content.replace('id: skill.remember', 'id: skill.memory.remember')
    content = content.replace('id: skill.recall', 'id: skill.memory.recall')
    content = content.replace('id: skill.forget', 'id: skill.memory.forget')
    content = content.replace('id: skill.recap', 'id: skill.memory.recap')
    content = content.replace('id: skill.session_history', 'id: skill.memory.session_history')
    content = content.replace('id: skill.commit_history', 'id: skill.memory.commit_history')
    content = content.replace('id: skill.commit_context', 'id: skill.memory.commit_context')

    content = content.replace('id: skill.guardrail', 'id: skill.quality.guardrail')
    content = content.replace('id: skill.sql_analyzer', 'id: skill.quality.sql')
    content = content.replace('id: skill.korean_metadata', 'id: skill.quality.korean_metadata')
    content = content.replace('id: skill.receiving_code_review', 'id: skill.quality.receive_review')
    content = content.replace('id: skill.requesting_code_review', 'id: skill.quality.request_review')
    content = content.replace('id: skill.verification_before_completion', 'id: skill.quality.verify_completion')

    content = content.replace('id: skill.developing_with_streamlit', 'id: skill.development.streamlit')
    content = content.replace('id: skill.frontend_design', 'id: skill.development.design')
    content = content.replace('id: skill.test_driven_development', 'id: skill.development.tdd')
    content = content.replace('id: skill.using_git_worktrees', 'id: skill.development.worktrees')
    content = content.replace('id: skill.systematic_debugging', 'id: skill.development.debugging')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] {filepath}")

def main():
    root_dir = "/home/jumasi/workstation/.agents"
    
    # .agents 내부 전체 파이썬 및 마크다운 파일 탐색하여 갱신
    for root, dirs, files in os.walk(root_dir):
        # 불필요한 디렉토리 탐색 차단
        dirs[:] = [d for d in dirs if d not in {".git", ".github", "scratch", "node_modules", ".venv", "__pycache__"}]
        for file in files:
            if file.endswith(".md") or file.endswith(".py"):
                filepath = os.path.join(root, file)
                replace_in_file(filepath)

if __name__ == '__main__':
    main()
