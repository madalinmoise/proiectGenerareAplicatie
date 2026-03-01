#!/usr/bin/env python3
"""
Final targeted mojibake fixer v3 — uses exact string replacement for remaining patterns.
"""
import os, sys

# These are the exact byte sequences that appear in the files after partial earlier fixing.
# Each key is the garbled string, each value is the correct UTF-8 character.
REPLACEMENTS = [
    # Order matters — longer patterns first to avoid partial matches
    # Î (capital Romanian I-hat) — was: ÃŽ
    ('ÃŽ', 'Î'),
    # ă — was: Ä› or Äƒ (seen as Ä followed by ƒ U+0192)
    ('Ä\u0192', 'ă'),   # Ä + LATIN SMALL LETTER F WITH HOOK
    ('Äƒ', 'ă'),        # alternate encoding
    # Ă (uppercase) — was: Ĥ or Ä‚
    ('Ä\u201a', 'Ă'),   # Ä + SINGLE LOW-9 QUOTATION MARK
    ('Ä‚', 'Ă'),
    # â — was: Ã¢
    ('Ã¢', 'â'),
    # Â (capital) — was: Ã‚
    ('Ã‚', 'Â'),
    # în — was: Ã®n
    ('Ã®', 'î'),
    # ș — was: È™ or Èš or Ȟ
    ('È\u2122', 'Ș'),  # Ș (uppercase, seen in some files)
    ('È™', 'ș'),       # ș lowercase
    ('Èš', 'ț'),       # ț
    ('È\u203a', 'ș'),   # alternate
    # Ș uppercase — was: È˜
    ('È˜', 'Ș'),
    # Ț uppercase — was: Èš or Ȟ  
    ('Èš', 'Ț'),
    # ț lowercase — various forms
    ('È›', 'ț'),
    # Ã (without a combining char) — only lone ones (corner cases)
]

def fix_text(text):
    for bad, good in REPLACEMENTS:
        if bad in text:
            text = text.replace(bad, good)
    return text

def needs_fix(text):
    return any(bad in text for bad, _ in REPLACEMENTS)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        original = f.read()
    
    if not needs_fix(original):
        return False, 0
    
    fixed = fix_text(original)
    changed_lines = sum(1 for a, b in zip(original.splitlines(), fixed.splitlines()) if a != b)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed)
    
    return True, changed_lines

def main():
    base_dir = r"c:\Users\Administrator\Downloads\program expert"
    
    py_files = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', 'Backup', '.git')]
        for fname in files:
            if fname.endswith('.py') and fname not in ('fix_encoding.py', 'fix_encoding_v2.py', 'fix_encoding_v3.py'):
                py_files.append(os.path.join(root, fname))
    
    print(f"Scanning {len(py_files)} Python files...\n")
    fixed_total = 0
    for fpath in sorted(py_files):
        rel = os.path.relpath(fpath, base_dir)
        changed, lines = process_file(fpath)
        if changed:
            print(f"  [FIXED {lines:3d} lines] {rel}")
            fixed_total += 1
    
    print(f"\nFixed {fixed_total} files.")
    
    # Verify
    print("\n--- Final Verification ---")
    bad_files = 0
    for fpath in py_files:
        rel = os.path.relpath(fpath, base_dir)
        with open(fpath, encoding='utf-8', errors='replace') as f:
            src = f.read()
        remaining = [bad for bad, _ in REPLACEMENTS if bad in src]
        if remaining:
            print(f"  [STILL BAD] {rel}: {remaining[:3]}")
            bad_files += 1
    
    if bad_files == 0:
        print("  All files clean!")
    else:
        # Show a sample of remaining issues for manual review
        print(f"\n  {bad_files} files need manual inspection.")

if __name__ == '__main__':
    main()
