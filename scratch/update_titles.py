import os
import re

directories = [
    '/home/jumasi/workstation/.agents/rules',
    '/home/jumasi/workstation/.agents/indexes',
    '/home/jumasi/workstation/.agents/principles'
]

# Mapping rules for title conversion
# [Rule]
rule_mappings = {
    'rules-index.md': '[Index] 에이전트 룰 허브',
    'L1-git.md': '[Rule] Git 및 커밋 표준',
    'L2-architecture.md': '[Rule] 아키텍처 3계층 설계',
    'L2-business-constants.md': '[Rule] 비즈니스 상수 매핑',
    'L2-color-system.md': '[Rule] 컬러 및 시각화 시스템',
    'L2-context-readability.md': '[Rule] 코드 가독성 최적화',
    'L2-metadata-standard.md': '[Rule] 옵시디언 메타데이터 표준',
    'L2-naming-convention.md': '[Rule] 코드 명명 규칙',
    'L2-sync-policy.md': '[Rule] 자산 동기화 정책',
    'L3-dashboard.md': '[Rule] Streamlit UI 구성',
    'L3-plot.md': '[Rule] Plotly 시각화 격리',
    'L3-query.md': '[Rule] SQL 쿼리 작성 표준',
    'L3-service.md': '[Rule] 비즈니스 서비스 전처리'
}

# [Index]
index_mappings = {
    'Agent Index.md': '[Index] 에이전트 허브',
    'Architecture Index.md': '[Index] 아키텍처 허브',
    'Business Domain Index.md': '[Index] 비즈니스 도메인 허브',
    'Home.md': '[Index] 통합 지식 홈',
    'Rule Index.md': '[Index] 룰 허브',
    'Skill Index.md': '[Index] 스킬 허브',
    'Wiki Index.md': '[Index] 위키 통합 허브'
}

# [Wiki] / [Principle]
principle_mappings = {
    'Knowledge Curation.md': '[Wiki] 지식 큐레이션 철학'
}

all_mappings = {**rule_mappings, **index_mappings, **principle_mappings}

def update_title(file_path, new_title):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match the frontmatter title
    # We look for ^title: ".*"$ or ^title: .*$
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

for d in directories:
    if os.path.exists(d):
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith('.md'):
                    if file in all_mappings:
                        update_title(os.path.join(root, file), all_mappings[file])
                    else:
                        print(f"No mapping found for {file}, skipping...")

