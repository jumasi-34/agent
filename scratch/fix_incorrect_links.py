#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

WORKSPACE_ROOT = "/home/jumasi/workstation"
AGENTS_DIR = os.path.join(WORKSPACE_ROOT, ".agents")

# 잘못된 치환 패턴 매핑
# (잘못된 문자열, 올바른 문자열)
CORRECTIONS = [
    # guide-index.md 오매칭 교정
    ("context/evals/guide-index.md", "context/evals/evals-index.md"),
    ("context/guide/guide-index.md", "context/guide/guide-index.md"),
    ("context/domain/guide-index.md", "context/domain/domain-index.md"),
    ("context/prd/guide-index.md", "context/prd/prd-index.md"),
    ("context/checklist/guide-index.md", "context/checklist/checklist-index.md"),
    ("context/infra/guide-index.md", "context/infra/infra-index.md"),
    ("rules/guide-index.md", "rules/rules-index.md"),
    
    # 상대 경로 교정
    ("../evals/guide-index.md", "../evals/evals-index.md"),
    ("../domain/guide-index.md", "../domain/domain-index.md"),
    ("../prd/guide-index.md", "../prd/prd-index.md"),
    ("../checklist/guide-index.md", "../checklist/checklist-index.md"),
    ("../infra/guide-index.md", "../infra/infra-index.md"),
    ("../rules/guide-index.md", "../rules/rules-index.md"),
]

def main():
    print("Fixing incorrect index.md link replacements...")
    
    for root, dirs, files in os.walk(AGENTS_DIR):
        for file in files:
            if not file.endswith(".md"):
                continue
            
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            modified = False
            for bad, good in CORRECTIONS:
                if bad in content:
                    content = content.replace(bad, good)
                    modified = True
            
            if modified:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed links in: {os.path.relpath(file_path, AGENTS_DIR)}")

    print("Fixing completed.")

if __name__ == "__main__":
    main()
