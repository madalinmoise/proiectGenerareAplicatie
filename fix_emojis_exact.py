import os

EMOJI_FIXES = {
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '↩': '↩',
    ''↓', # mostly likely 
    # any other versions with trailing spaces
    '': '',
}

def main():
    base_dir = r"c:\Users\Administrator\Downloads\program expert"
    changed_count = 0
    
    for root, _, files in os.walk(base_dir):
        if 'Backup' in root.split(os.sep): continue
        for fname in files:
            if fname.endswith('.py'):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    original = text
                    for bad, good in EMOJI_FIXES.items():
                        text = text.replace(bad, good)
                        
                    if text != original:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(text)
                        print(f"Fixed {fname}")
                        changed_count += 1
                except Exception as e:
                    pass

    print(f"Done. Fixed emojis in {changed_count} files.")

if __name__ == '__main__':
    main()
