import os

def parse_md_table(filepath: str) -> list[dict]:
    """Pure, stateless callable to parse GitHub Flavored Markdown tables."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    in_table = False
    headers = []
    rows = []
    for line in lines:
        line = line.strip()
        if line.startswith('|') and line.endswith('|'):
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if not in_table:
                headers = cols
                in_table = True
            elif all(c.replace('-', '').strip() == '' for c in cols):
                pass
            else:
                row = dict(zip(headers, cols))
                rows.append(row)
        else:
            in_table = False
    return rows
