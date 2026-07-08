import os
import re

TEST_DIR = "tests"

def process_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Match `MagicMock(stdout=...)` only if not preceded by `returncode=...`
    # We can just match MagicMock(stdout=...) and then carefully replace it if returncode is not in the same line
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if 'MagicMock(stdout=' in line and 'returncode=' not in line:
            line = line.replace('MagicMock(stdout=', 'MagicMock(returncode=0, stdout=')
        
        # also match empty MagicMock() for typical variable names
        if re.search(r'(mock_proc\s*=\s*MagicMock)\(\)', line):
            line = re.sub(r'(mock_proc\s*=\s*MagicMock)\(\)', r'\1(returncode=0)', line)
        if re.search(r'(mock_res\s*=\s*MagicMock)\(\)', line):
            line = re.sub(r'(mock_res\s*=\s*MagicMock)\(\)', r'\1(returncode=0)', line)
        if re.search(r'(mock_result\s*=\s*MagicMock)\(\)', line):
            line = re.sub(r'(mock_result\s*=\s*MagicMock)\(\)', r'\1(returncode=0)', line)
        if re.search(r'^\s*(mock\s*=\s*MagicMock)\(\)', line):
            line = re.sub(r'(mock\s*=\s*MagicMock)\(\)', r'\1(returncode=0)', line)
        if re.search(r'(mock_close\s*=\s*MagicMock)\(\)', line):
            line = re.sub(r'(mock_close\s*=\s*MagicMock)\(\)', r'\1(returncode=0)', line)
        if re.search(r'(mock_remove\s*=\s*MagicMock)\(\)', line):
            line = re.sub(r'(mock_remove\s*=\s*MagicMock)\(\)', r'\1(returncode=0)', line)
            
        # specifically for test_git_client.py detached HEAD test
        if 'show_current_res = MagicMock(stdout=' in line and 'returncode' not in line:
            line = line.replace('show_current_res = MagicMock(stdout=', 'show_current_res = MagicMock(returncode=0, stdout=')
        if 'head_res = MagicMock(stdout=' in line and 'returncode' not in line:
            line = line.replace('head_res = MagicMock(stdout=', 'head_res = MagicMock(returncode=0, stdout=')
        if 'origin_main_res = MagicMock(stdout=' in line and 'returncode' not in line:
            line = line.replace('origin_main_res = MagicMock(stdout=', 'origin_main_res = MagicMock(returncode=0, stdout=')
        if 'main_res = MagicMock(stdout=' in line and 'returncode' not in line:
            line = line.replace('main_res = MagicMock(stdout=', 'main_res = MagicMock(returncode=0, stdout=')

        new_lines.append(line)
        
    with open(filepath, "w") as f:
        f.write('\n'.join(new_lines))

for root, dirs, files in os.walk(TEST_DIR):
    for file in files:
        if file.endswith(".py"):
            process_file(os.path.join(root, file))

print("Done fixing MagicMocks!")
