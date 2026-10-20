#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_fanqie_quality.py
-----------------------
Automated Quality Audit Tool for Fanqie Webnovel Signing Review.
Checks character counts, formatting, book title marks, calendar openers,
dialogue quotation density, encoding, and AI slop patterns.

Standard Library only. Compatible with Python 3.7+.
"""

import argparse
import os
import re
import sys
from typing import Dict, List, Tuple

# Configuration & Thresholds
CHAR_MIN = 2050
CHAR_MAX = 4000
MIN_DIALOGUE_QUOTES = 18

RE_MARKDOWN_HEADER = re.compile(r'^\s*#{1,6}\s+', re.MULTILINE)
RE_MARKDOWN_EMPHASIS = re.compile(r'(\*{1,2}|_{1,2})[^\n*]+?\1')
RE_MARKDOWN_BLOCKQUOTE = re.compile(r'^\s*>\s+', re.MULTILINE)
RE_MARKDOWN_LIST = re.compile(r'^\s*[-*+]\s+', re.MULTILINE)
RE_MARKDOWN_CODE = re.compile(r'(`{1,3})[^\n`]+?\1')

RE_BOOK_TITLE_MARK = re.compile(r'《[^》\n]{1,60}》')
RE_CALENDAR_WEATHER = re.compile(
    r'^\s*[0-9一二三四五六七八九十百]+月[0-9一二三四五六七八九十]+[日号]?.*?(清晨|一早|午后|傍晚|深夜|微风|寒霜|秋阳|晨雾|雨水)'
)
RE_AI_SLOP_ENDINGS = re.compile(r'（全书完）|时代大幕|拉开了大幕|这不仅是.*?更是|仰不愧于天')
RE_ACCOUNTING_NEGATION = re.compile(r'并非[^\n，。]{1,20}而是|不是[^\n，。]{1,20}乃是')
RE_LATIN1_CORRUPTION = re.compile(r'ã€|â€|Ã©|Ã¨|Ã|å|æ')

def count_non_newline_chars(text: str) -> int:
    return len(re.sub(r'\s+', '', text))

def count_dialogue_quotes(text: str) -> int:
    # Count occurrences of Chinese quotes “ ... ”
    left_quotes = text.count('“')
    right_quotes = text.count('”')
    return min(left_quotes, right_quotes)

def audit_file(filepath: str) -> Dict[str, any]:
    basename = os.path.basename(filepath)
    issues = []
    warnings = []

    # Check filename for book title marks
    if '《' in basename or '》' in basename:
        issues.append(f"Filename contains book title marks 《》: '{basename}'")

    # Read binary to verify encoding and BOM
    try:
        with open(filepath, 'rb') as f:
            raw_bytes = f.read()
    except Exception as e:
        return {'file': basename, 'status': 'FAIL', 'issues': [f"Read error: {e}"], 'warnings': []}

    if raw_bytes.startswith(b'\xef\xbb\xbf'):
        issues.append("File starts with UTF-8 BOM (Byte Order Mark). Should be UTF-8 no-BOM.")

    if b'\r' in raw_bytes:
        warnings.append("File contains Windows CRLF or CR line endings. Recommended LF.")

    try:
        text = raw_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        issues.append(f"UTF-8 decode failed: {e}")
        return {'file': basename, 'status': 'FAIL', 'issues': issues, 'warnings': warnings}

    # Check Latin-1 corruption patterns
    latin1_match = RE_LATIN1_CORRUPTION.findall(text)
    if latin1_match and len(latin1_match) > 3:
        issues.append(f"Potential Latin-1 encoding corruption detected ({len(latin1_match)} instances, e.g. '{latin1_match[0]}').")

    # Character count
    non_ws_count = count_non_newline_chars(text)
    if non_ws_count < CHAR_MIN:
        issues.append(f"Character count too low: {non_ws_count} chars (min: {CHAR_MIN}).")
    elif non_ws_count > CHAR_MAX:
        warnings.append(f"Character count high: {non_ws_count} chars (recommended < {CHAR_MAX}).")

    # Markdown checks
    if RE_MARKDOWN_HEADER.search(text):
        issues.append("Markdown header syntax (# ...) detected in body.")
    if RE_MARKDOWN_EMPHASIS.search(text):
        issues.append("Markdown bold/italic syntax (**...**) detected in body.")
    if RE_MARKDOWN_BLOCKQUOTE.search(text):
        issues.append("Markdown blockquote syntax (> ...) detected in body.")
    if RE_MARKDOWN_LIST.search(text):
        issues.append("Markdown list syntax (-/+ ...) detected in body.")
    if RE_MARKDOWN_CODE.search(text):
        issues.append("Markdown code syntax (`...`) detected in body.")

    # Book title marks in body
    book_marks = RE_BOOK_TITLE_MARK.findall(text)
    if book_marks:
        issues.append(f"Book title marks 《》 detected in body ({len(book_marks)} instances, e.g. '{book_marks[0]}').")

    # Calendar-weather opening
    first_non_empty_line = ""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            first_non_empty_line = stripped
            break
    if RE_CALENDAR_WEATHER.search(first_non_empty_line):
        warnings.append(f"Calendar-weather template opening detected: '{first_non_empty_line[:40]}...'")

    # AI slop endings
    last_non_empty_line = ""
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if stripped:
            last_non_empty_line = stripped
            break
    if RE_AI_SLOP_ENDINGS.search(last_non_empty_line) or '（全书完）' in text:
        issues.append("AI slop ending or mechanical '（全书完）' tag detected.")

    # Dialogue density
    quote_pairs = count_dialogue_quotes(text)
    if quote_pairs < MIN_DIALOGUE_QUOTES:
        warnings.append(f"Low dialogue density: {quote_pairs} quote pairs (recommended >= {MIN_DIALOGUE_QUOTES}).")

    # Accounting prose negation
    neg_matches = RE_ACCOUNTING_NEGATION.findall(text)
    if len(neg_matches) >= 3:
        warnings.append(f"Dense '并非……而是……' negation prose detected ({len(neg_matches)} instances).")

    status = 'FAIL' if issues else ('WARN' if warnings else 'PASS')
    return {
        'file': basename,
        'chars': non_ws_count,
        'quotes': quote_pairs,
        'status': status,
        'issues': issues,
        'warnings': warnings
    }

def main():
    parser = argparse.ArgumentParser(description="Audit novel files for Fanqie signing review standards.")
    parser.add_argument('--dir', type=str, help="Directory containing novel chapter files (.md / .txt)")
    parser.add_argument('--file', type=str, help="Single chapter file to audit")
    parser.add_argument('--strict', action='store_true', help="Treat warnings as failures")
    args = parser.parse_args()

    if not args.dir and not args.file:
        parser.print_help()
        sys.exit(1)

    files_to_check = []
    if args.file:
        files_to_check.append(args.file)
    elif args.dir:
        for root, _, filenames in os.walk(args.dir):
            for fname in sorted(filenames):
                if fname.endswith(('.md', '.txt')) and not fname.startswith('.'):
                    files_to_check.append(os.path.join(root, fname))

    if not files_to_check:
        print("No chapter files found.")
        sys.exit(1)

    print(f"\n==================================================")
    print(f" FANQIE SIGNING QUALITY AUDIT TOOL")
    print(f" Target files: {len(files_to_check)}")
    print(f"==================================================\n")

    passed_count = 0
    warn_count = 0
    fail_count = 0
    total_chars = 0

    for filepath in files_to_check:
        res = audit_file(filepath)
        total_chars += res.get('chars', 0)
        status = res['status']

        if args.strict and status == 'WARN':
            status = 'FAIL'

        if status == 'PASS':
            passed_count += 1
            print(f" [PASS] {res['file']:<35} | {res['chars']} chars | {res['quotes']} quotes")
        elif status == 'WARN':
            warn_count += 1
            print(f" [WARN] {res['file']:<35} | {res['chars']} chars | {res['quotes']} quotes")
            for w in res['warnings']:
                print(f"        -> WARN: {w}")
        else:
            fail_count += 1
            print(f" [FAIL] {res['file']:<35} | {res.get('chars', 0)} chars")
            for issue in res['issues']:
                print(f"        !! FAIL: {issue}")
            for w in res['warnings']:
                print(f"        -> WARN: {w}")

    print(f"\n--------------------------------------------------")
    print(f" AUDIT SUMMARY:")
    print(f" Total Chapters : {len(files_to_check)}")
    print(f" Total Chars    : {total_chars:,}")
    print(f" Passed         : {passed_count}")
    print(f" Warnings       : {warn_count}")
    print(f" Failed         : {fail_count}")
    print(f"--------------------------------------------------")

    if fail_count > 0:
        print("\nResult: FAILED - Quality gates not passed.\n")
        sys.exit(1)
    elif warn_count > 0 and args.strict:
        print("\nResult: FAILED (strict mode) - Warnings present.\n")
        sys.exit(1)
    else:
        print("\nResult: SUCCESS - All chapters meet Fanqie signing criteria.\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
