import os
import re

def clean_ui_text(content):
    """
    Remove any emojis, garbled unicode (mojibake), and non-Romanian special characters
    from Tkinter widget texts (buttons, labels, tabs).
    We want a clean, professional UI without emojis to avoid encoding problems.
    """
    # Characters that are allowed: ASCII, Romanian letters
    # We will identify strings like text="Salvează config" and clean the start of the string
    
    lines = content.split('\n')
    for i in range(len(lines)):
        # Find parts like text="something" or .add("something") or .set("something")
        
        # We can just look for ["']([^"']*)["'] and clean the inside if it matches typical UI text locations
        # But a safer way is to just strip out known bad prefixes or any character outside of our whitelist 
        # that appears before the first normal letter.
        
        # A simpler approach: regex replace any garbled CP1252/UTF8 double encoded emoji prefixes
        # like , , etc.
        lines[i] = re.sub(r''', lines[i])
        lines[i] = re.sub(r'\s*', '', lines[i])
        lines[i] = re.sub(r'\s*', '', lines[i])
        lines[i] = re.sub(r''', lines[i])
        lines[i] = re.sub(r'\s*', '', lines[i])
        lines[i] = re.sub(r'\s*', '', lines[i])
        lines[i] = re.sub(r''', lines[i])
        
        # Also remove actual emojis we might have fixed earlier
        lines[i] = re.sub(r'[]\s*', '', lines[i])
        lines[i] = re.sub(r'\s*', '', lines[i]) # variant selector
        
    return '\n'.join(lines)

def main():
    base_dir = r"c:\Users\Administrator\Downloads\program expert"
    changed_count = 0
    
    for root, _, files in os.walk(base_dir):
        if 'Backup' in root.split(os.sep): continue
        if '.git' in root.split(os.sep): continue
        
        for fname in files:
            if fname.endswith('.py'):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    cleaned = clean_ui_text(text)
                        
                    if cleaned != text:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(cleaned)
                        print(f"Cleaned UI text in {fname}")
                        changed_count += 1
                except Exception as e:
                    pass

    print(f"Done. Cleaned {changed_count} files.")

if __name__ == '__main__':
    main()
