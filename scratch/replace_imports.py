import os
import re
import glob

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # We want to replace 'orchestrator' -> 'kernel' and 'skills' -> 'drivers'
    # Specifically for imports and module accesses.
    
    # 1. from orchestrator import
    content = re.sub(r'\bfrom orchestrator\b', 'from kernel', content)
    # 2. import orchestrator
    content = re.sub(r'\bimport orchestrator\b', 'import kernel', content)
    # 3. orchestrator.module
    content = re.sub(r'\borchestrator\.', 'kernel.', content)
    
    # 4. from skills import
    content = re.sub(r'\bfrom skills\b', 'from drivers', content)
    # 5. import skills
    content = re.sub(r'\bimport skills\b', 'import drivers', content)
    # 6. skills.module
    content = re.sub(r'\bskills\.', 'drivers.', content)
    
    # General word replacements for markdown
    content = re.sub(r'\borchestrator/', 'kernel/', content)
    content = re.sub(r'\bskills/', 'drivers/', content)
    content = re.sub(r'`orchestrator`', '`kernel`', content)
    content = re.sub(r'`skills`', '`drivers`', content)

    with open(filepath, 'w') as f:
        f.write(content)

def main():
    search_dirs = ['kb', '.']
    
    for dir_name in search_dirs:
        for root, _, files in os.walk(dir_name):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    process_file(filepath)

if __name__ == '__main__':
    main()
