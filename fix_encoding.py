#!/usr/bin/env python3
"""
Fix mojibake (double-encoded UTF-8 read as latin-1) in all .py files.
Detects UTF-8 bytes that were interpreted as cp1252, then re-encodes correctly.
"""

import os
import sys

def fix_mojibake(text):
    """Try to fix cp1252/latin-1 -> utf-8 mojibake."""
    try:
        # Encode back to bytes using latin-1 (how it was incorrectly decoded),
        # then decode as UTF-8 (the original encoding).
        fixed = text.encode('latin-1').decode('utf-8')
        return fixed, True
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text, False

def process_file(filepath):
    # Read file as latin-1 first to get raw bytes as text
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()
    
    # Check if it has mojibake patterns by looking for common garbled sequences
    mojibake_indicators = [
        'Ä', 'Ã', 'È', 'É', 'Å', 'Â',
        '\u00c3', '\u00e2', '\u00c8',
    ]
    
    has_mojibake = any(m in original for m in mojibake_indicators)
    if not has_mojibake:
        return False, "no mojibake detected"
    
    # Try to fix by re-reading as latin-1 and decoding as utf-8
    try:
        with open(filepath, 'rb') as f:
            raw_bytes = f.read()
        
        # Decode as latin-1/cp1252 to get text that was incorrectly encoded
        as_latin1 = raw_bytes.decode('latin-1')
        
        # Try to fix line by line (some lines may be pure ASCII, some mojibake)
        fixed_lines = []
        changed = False
        for line in as_latin1.splitlines(keepends=True):
            fixed_line, was_fixed = fix_mojibake(line)
            fixed_lines.append(fixed_line)
            if was_fixed and fixed_line != line:
                changed = True
        
        if not changed:
            return False, "could not fix (mixed encoding)"
        
        fixed_text = ''.join(fixed_lines)
        
        # Write back as UTF-8
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_text)
        
        return True, f"fixed"
    
    except Exception as e:
        return False, f"error: {e}"

def main():
    base_dir = r"c:\Users\Administrator\Downloads\program expert"
    
    py_files = []
    for root, dirs, files in os.walk(base_dir):
        # Skip __pycache__ and hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and d != 'Backup']
        for fname in files:
            if fname.endswith('.py'):
                py_files.append(os.path.join(root, fname))
    
    print(f"Found {len(py_files)} .py files to check\n")
    
    fixed_count = 0
    for fpath in py_files:
        rel = os.path.relpath(fpath, base_dir)
        success, msg = process_file(fpath)
        if success:
            print(f"  [FIXED] {rel}")
            fixed_count += 1
        elif 'mojibake' not in msg:
            print(f"  ~ skip: {rel} ({msg})")
    
    print(f"\nDone. Fixed {fixed_count} files.")

if __name__ == '__main__':
    main()
