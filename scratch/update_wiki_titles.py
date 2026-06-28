import os
import re

directory = '/home/jumasi/workstation/.agents/wiki'

# [Wiki]
wiki_mappings = {
    'Agent Collaboration & Memory.md': '[Wiki] 에이전트 협업 및 기억',
    'Architecture Guide.md': '[Wiki] 아키텍처 3계층 가이드',
    'Error Isolation & Logging Standard.md': '[Wiki] 에러 격리 및 로깅',
    'Git Dual Push & Rsync Sync.md': '[Wiki] 듀얼 푸시 및 동기화',
    'Harness Testing & Quality Gate.md': '[Wiki] 품질 게이트 검증',
    'Natural Language Humanizing Rule.md': '[Wiki] AI 문체 정제 규칙',
    'PRD Planning Workflow.md': '[Wiki] PRD 기획 워크플로우',
    'Plotly Visualization System.md': '[Wiki] 시각화 시스템 설계',
    'Project Knowledge Graph & Curation.md': '[Wiki] 지식 그래프 큐레이션',
    'Quality Metric & Business Rules.md': '[Wiki] 품질 지표 및 비즈니스 수식',
    'Streamlit UI Development.md': '[Wiki] Streamlit UI 개발'
}

def update_title(file_path, new_title):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r'^title:\s*(".*"|.*)$', re.MULTILINE)
    
    if pattern.search(content):
        new_content = pattern.sub(f'title: "{new_title}"', content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated title for: {os.path.basename(file_path)} -> {new_title}")
    else:
        # If no title exists, insert it after the first ---
        pattern_yaml = re.compile(r'^---\n', re.MULTILINE)
        match = pattern_yaml.search(content)
        if match:
            insertion_point = match.end()
            new_content = content[:insertion_point] + f'title: "{new_title}"\n' + content[insertion_point:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Inserted title for: {os.path.basename(file_path)} -> {new_title}")
        else:
            # If no frontmatter, create one
            new_content = f'---\ntitle: "{new_title}"\n---\n\n{content}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Created frontmatter and title for: {os.path.basename(file_path)} -> {new_title}")

if os.path.exists(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                if file in wiki_mappings:
                    update_title(os.path.join(root, file), wiki_mappings[file])
                else:
                    print(f"No mapping found for {file}, skipping...")

