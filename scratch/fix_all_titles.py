import os
import re
from pathlib import Path

agents_dir = Path("/home/jumasi/workstation/.agents")

def generate_title_from_filename(filename, path_obj):
    name_without_ext = path_obj.stem
    
    if "skills" in path_obj.parts:
        # If it's a SKILL.md file, use its parent folder name for better context
        if name_without_ext == "SKILL":
            skill_name = path_obj.parent.name.replace("-", " ").title()
            return f"[Skill] {skill_name}"
        else:
            clean_name = name_without_ext.replace("-", " ").title()
            return f"[Skill] {clean_name}"
    elif "rules" in path_obj.parts:
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[Rule] {clean_name}"
    elif "wiki" in path_obj.parts:
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[Wiki] {clean_name}"
    elif "indexes" in path_obj.parts:
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[Index] {clean_name}"
    elif "principles" in path_obj.parts:
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[Principle] {clean_name}"
    elif "raw" in path_obj.parts:
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[Raw] {clean_name}"
    elif "context" in path_obj.parts:
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[Context] {clean_name}"
    else:
        # Default fallback
        clean_name = name_without_ext.replace("-", " ").title()
        return f"[{clean_name}]"

def fix_title(file_path):
    path_obj = Path(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files that already have our standard bracket titles
    title_pattern = re.compile(r'^title:\s*"?(\[[A-Za-z]+\]\s+.*?)"?$', re.MULTILINE)
    if title_pattern.search(content):
        return False
        
    new_title = generate_title_from_filename(path_obj.name, path_obj)
    
    # Check if there is an existing title field
    existing_title_pattern = re.compile(r'^title:\s*(".*"|.*)$', re.MULTILINE)
    
    if existing_title_pattern.search(content):
        # Update existing title
        new_content = existing_title_pattern.sub(f'title: "{new_title}"', content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated title: {path_obj.name} -> {new_title}")
        return True
    else:
        # Check if there's existing frontmatter
        yaml_pattern = re.compile(r'^---\n', re.MULTILINE)
        match = yaml_pattern.search(content)
        if match:
            # Insert title right after first ---
            insertion_point = match.end()
            new_content = content[:insertion_point] + f'title: "{new_title}"\n' + content[insertion_point:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Inserted title: {path_obj.name} -> {new_title}")
            return True
        else:
            # Create new frontmatter at top
            new_content = f'---\ntitle: "{new_title}"\n---\n\n{content}'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Created frontmatter: {path_obj.name} -> {new_title}")
            return True

updated_count = 0
for file_path in agents_dir.rglob("*.md"):
    if ".obsidian" in file_path.parts:
        continue
    if fix_title(file_path):
        updated_count += 1

print(f"\nTotal files updated: {updated_count}")
