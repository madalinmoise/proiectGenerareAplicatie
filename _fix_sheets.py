import re

path = r'c:\Users\Administrator\Downloads\program expert\app.py'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of sheets_listbox in preview_document and similar
pattern = r"        selected = self\.sheets_listbox\.curselection\(\)\r?\n        if not selected:\r?\n            messagebox\.showerror\([^)]+\)\r?\n            return\r?\n        sheet = self\.sheets_listbox\.get\(selected\[0\]\)\r?\n        try:\r?\n            df = pd\.read_excel\(data_file, sheet_name=sheet\)"
replacement = '        try:\n            df = pd.read_excel(data_file, sheet_name=0)'

new_content = re.sub(pattern, replacement, content)
changed = content.count('sheets_listbox') - new_content.count('sheets_listbox')
print(f'Replaced {changed} occurrences. Remaining: {new_content.count("sheets_listbox")}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
