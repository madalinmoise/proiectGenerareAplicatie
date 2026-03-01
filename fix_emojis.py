import os

def fix_emoji_mojibake(text):
    """
    Fix emoji mojibake that was caused by UTF-8 bytes being interpreted as cp1252.
    For example: (F0 9F 9A 80) read as cp1252 becomes 
    """
    # Find all sequences starting with or â
    # It's safer to just try converting the whole text line by line
    fixed_lines = []
    changed_any = False
    
    for line in text.splitlines(keepends=True):
        if 'in line or 'in line or 'in line.lower() or '' in line:
            try:
                fixed_line = line.encode('cp1252').decode('utf-8')
                fixed_lines.append(fixed_line)
                changed_any = True
            except (UnicodeEncodeError, UnicodeDecodeError):
                # If the line can't be cleanly converted, don't touch it
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
            
    return ''.join(fixed_lines), changed_any

def main():
    base_dir = r"c:\Users\Administrator\Downloads\program expert"
    changed_files = 0
    
    for root, dirs, files in os.walk(base_dir):
        # skip Backup
        if 'Backup' in root.split(os.sep):
            continue
        for fname in files:
            if fname.endswith('.py'):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    fixed_text, changed = fix_emoji_mojibake(text)
                    if changed:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(fixed_text)
                        print(f"Fixed emojis in: {os.path.relpath(fpath, base_dir)}")
                        changed_files += 1
                except Exception as e:
                    print(f"Error on {fname}: {e}")

    print(f"Done. Fixed {changed_files} files.")

if __name__ == '__main__':
    main()
