import os
import re

files_to_clean = ['tabs/ai_guide_tab.py', 'tabs/reports_tab.py', 'tabs/extract_tab.py']
for f in files_to_clean:
    filepath = os.path.join(r'c:\Users\Administrator\Downloads\program expert', f)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Simple removal of obvious mojibake symbols
        text = text.replace('âš   ', '')
        text = text.replace('âš™  ', '')
        text = text.replace('â “ ', '')
        text = text.replace('âš¡ ', '')
        text = text.replace('â‡  ', '')
        text = text.replace('âœ– ', '')
        text = text.replace('âœ✨ ', '')

        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)
        
        print(f"Cleaned {f}")
