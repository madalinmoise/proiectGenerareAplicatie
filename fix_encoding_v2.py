#!/usr/bin/env python3
"""
Robust mojibake fixer v2 — fixes garbled Romanian text in Python files.
Handles mixed encoding: fixes only the garbled substrings within each line.

Mojibake pattern: UTF-8 bytes were saved but the file was read/written as cp1252,
producing sequences like: gÄƒsit -> găsit, Ã®n -> în, È™ablon -> șablon
"""

import os
import re
import sys

# Mapping of common garbled Romanian sequences to correct chars
# Generated from: each Romanian char encoded as UTF-8, bytes decoded as cp1252
FIXES = {
    # ă (0xC4 0x83 in UTF-8 -> latin-1: Ä ƒ)
    'Ä\x83': 'ă',   # ă
    'Ã\xa3': 'ã',
    # â (0xC3 0xA2 -> Ã â)
    'Ã¢': 'â',
    # î (0xC3 0xAE -> Ã®)
    'Ã®': 'î',
    # ș (0xC8 0x99 -> È™)
    'È\x99': 'ș',   # ș
    # ț (0xC8 0x9B -> È›)
    'È\x9b': 'ț',   # ț
    # Ă (0xC4 0x82 -> Ä‚)
    'Ä\x82': 'Ă',
    # Â (0xC3 0x82 -> Â)
    'Ã\x82': 'Â',
    # Î (0xC3 0x8E -> Î)
    'Ã\x8e': 'Î',
    # Ș (0xC8 0x98 -> È˜)
    'È\x98': 'Ș',
    # Ț (0xC8 0x9A -> Èš)
    'È\x9a': 'Ț',
    # Also some that show as multi-char (when file was already partially fixed):
    'Ä\u203a': 'ă', # alternate form seen
    'È\u2122': 'ș',
    'È\u203a': 'ș',
    'Ã\xaf': 'ï',
    'Ã\xa0': 'à',
    # Quotes / dashes garbled
    'â\x80\x99': '\u2019',  # right single quote
    'â\x80\x9c': '\u201c',  # left double quote
    'â\x80\x9d': '\u201d',  # right double quote
    'â\x80\x93': '\u2013',  # en dash
    'â\x80\x94': '\u2014',  # em dash
}

def fix_line(line):
    """Fix mojibake in a single line by trying byte-level re-decode."""
    if not any(m in line for m in ['Ã', 'Ä', 'È', 'É', 'Â']):
        return line  # fast path: no mojibake chars

    # Strategy 1: try whole-line fix
    try:
        fixed = line.encode('latin-1').decode('utf-8')
        if fixed != line:
            return fixed
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass

    # Strategy 2: fix known patterns
    result = line
    for bad, good in FIXES.items():
        if bad in result:
            result = result.replace(bad, good)
    
    return result


def process_file(filepath):
    """Read, fix, and write a file. Returns (changed, num_lines_changed)."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='surrogateescape') as f:
            lines = f.readlines()
    except Exception as e:
        return False, 0, str(e)

    new_lines = []
    changed_count = 0
    for line in lines:
        fixed = fix_line(line)
        new_lines.append(fixed)
        if fixed != line:
            changed_count += 1

    if changed_count == 0:
        return False, 0, "clean"

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True, changed_count, "ok"
    except Exception as e:
        return False, 0, str(e)


def main():
    base_dir = r"c:\Users\Administrator\Downloads\program expert"

    py_files = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in ('__pycache__', 'Backup', '.git', 'checkpoints')]
        for fname in files:
            if fname.endswith('.py') and fname != 'fix_encoding_v2.py':
                py_files.append(os.path.join(root, fname))

    print(f"Checking {len(py_files)} Python files for mojibake...\n")

    fixed_total = 0
    for fpath in sorted(py_files):
        rel = os.path.relpath(fpath, base_dir)
        success, lines_changed, msg = process_file(fpath)
        if success:
            print(f"  [FIXED {lines_changed:3d} lines] {rel}")
            fixed_total += 1
        elif msg not in ('clean',):
            print(f"  [ERROR] {rel}: {msg}")

    print(f"\nDone. Fixed {fixed_total} files.")

    # Quick verification — check for remaining mojibake
    print("\n--- Verification ---")
    remaining = 0
    for fpath in py_files:
        rel = os.path.relpath(fpath, base_dir)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            src = f.read()
        bad = [c for c in ['Ã', 'Ä\x83', 'È\x99', 'È\x9b'] if c in src]
        if bad:
            print(f"  [STILL BAD] {rel}: {bad[:3]}")
            remaining += 1
    if remaining == 0:
        print("  All files are clean!")
    else:
        print(f"  {remaining} files still have issues.")


if __name__ == '__main__':
    main()
