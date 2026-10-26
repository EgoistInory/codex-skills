#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_fanqie_quality.py
-----------------------
Automated Quality Audit Tool for Fanqie Webnovel Signing & Recommendation Review.
Checks character counts, formatting, book title marks, calendar openers,
dialogue quotation density, encoding, micro AI slop phrases, omniscient clichés,
macro genre clashes, early chapter pacing, and paragraph burstiness.

Standard Library only. Compatible with Python 3.7+.
"""

import argparse
import math
import os
import re
import sys
from typing import Dict, List, Tuple

# Configuration & Thresholds
CHAR_MIN = 2050
CHAR_MAX = 4000
CHAR_STRICT_OVERLONG = 4500
CHAR_EARLY_CHAPTER_MAX = 3500
MIN_DIALOGUE_QUOTES = 18

RE_MARKDOWN_HEADER = re.compile(r'^\s*#{1,6}\s+', re.MULTILINE)
RE_MARKDOWN_EMPHASIS = re.compile(r'(\*{1,2}|_{1,2})[^\n*]+?\1')
RE_MARKDOWN_BLOCKQUOTE = re.compile(r'^\s*>\s+', re.MULTILINE)
RE_MARKDOWN_LIST = re.compile(r'^\s*[-*+]\s+', re.MULTILINE)
RE_MARKDOWN_CODE = re.compile(r'(`{1,3})[^\n`]+?\1')

RE_BOOK_TITLE_MARK = re.compile(r'《[^》\n]{1,60}》')
RE_REDUNDANT_TITLE_NUM = re.compile(r'第[0-9零一二两三四五六七八九十百千]+[章回节话]')
RE_BODY_FIRST_LINE_HEADER = re.compile(r'^(#{1,6}\s+|第\s*\d+\s*章|第[零一二两三四五六七八九十百千]+章)')
RE_CALENDAR_WEATHER = re.compile(
    r'^\s*[0-9一二三四五六七八九十百]+月[0-9一二三四五六七八九十]+[日号]?.*?(清晨|一早|午后|傍晚|深夜|微风|寒霜|秋阳|晨雾|雨水)'
)
RE_AI_SLOP_ENDINGS = re.compile(r'（全书完）|时代大幕|拉开了大幕|这不仅是.*?更是|仰不愧于天')
RE_ACCOUNTING_NEGATION = re.compile(r'并非[^\n，。]{1,20}而是|不是[^\n，。]{1,20}乃是')
RE_MICRO_AI_SLOP = re.compile(r'眼神.*?(?:闪过|复杂|警惕)|空气中弥漫|无形的气场|微妙的平衡|深知.*?意味|心中暗自|殊不知|随着时间的推移')
RE_OMNISCIENT_PROTAGONIST = re.compile(r'(?:早已料到|一切尽在掌握|算无遗策|胸有成竹|毫无悬念|早有预料|不出所料|皆在算中|洞若观火)')
RE_GENRE_CLASH_MACRO = re.compile(r'(?:金融保卫战|资本运作|跨周期|降维打击|市场下沉|货币战争|对冲风险|杠杆操作|资金池|产业升级)')
RE_LATIN1_CORRUPTION = re.compile(r'ã€|â€|Ã©|Ã¨|Ã|å|æ')

def count_non_newline_chars(text: str) -> int:
    return len(re.sub(r'\s+', '', text))

def count_dialogue_quotes(text: str) -> int:
    # Count occurrences of Chinese quotes “ ... ”
    left_quotes = text.count('“')
    right_quotes = text.count('”')
    return min(left_quotes, right_quotes)

def calculate_burstiness(paragraphs: List[str]) -> Tuple[float, float, int]:
    """Returns (mean_length, std_dev, short_paragraph_count)."""
    lengths = [len(re.sub(r'\s+', '', p)) for p in paragraphs if len(re.sub(r'\s+', '', p)) > 0]
    if not lengths:
        return 0.0, 0.0, 0
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    short_count = sum(1 for x in lengths if x < 20)
    return mean, std_dev, short_count

def audit_file(filepath: str) -> Dict[str, any]:
    basename = os.path.basename(filepath)
    issues = []
    warnings = []

    # Check filename for book title marks
    if '《' in basename or '》' in basename:
        issues.append(f"Filename contains book title marks 《》: '{basename}'")

    # Check filename prefix and redundant chapter numbers
    stem = os.path.splitext(basename)[0]
    if not re.match(r'^\d+[\s:：_\-]', basename):
        warnings.append(f"Filename '{basename}' lacks standard numeric prefix (e.g. '001-Title.md'), which may cause importer tools to fail to recognize chapters.")
    clean_title = re.sub(r'^\d+[\s:：_\-]+', '', stem)
    if RE_REDUNDANT_TITLE_NUM.search(clean_title):
        issues.append(f"Redundant chapter number in title: '{basename}' (contains duplicated chapter prefix like '第三十三章'). Title must only be the clean title text.")

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

    # Chapter index detection (e.g. 001 to 005)
    chapter_num_match = re.search(r'(?:ch|第)?(\d+)', stem, re.IGNORECASE)
    chapter_index = int(chapter_num_match.group(1)) if chapter_num_match else None

    # Character count checks
    non_ws_count = count_non_newline_chars(text)
    if non_ws_count < CHAR_MIN:
        issues.append(f"Character count too low: {non_ws_count} chars (min: {CHAR_MIN}).")
    elif non_ws_count > CHAR_STRICT_OVERLONG:
        warnings.append(f"Chapter severely overlong: {non_ws_count} chars (> {CHAR_STRICT_OVERLONG}). Critical risk of depressing mobile 15s retention and chapter completion rates.")
    elif non_ws_count > CHAR_MAX:
        warnings.append(f"Character count high: {non_ws_count} chars (recommended < {CHAR_MAX}).")

    if chapter_index is not None and 1 <= chapter_index <= 5 and non_ws_count > CHAR_EARLY_CHAPTER_MAX:
        warnings.append(f"Golden early chapter (Ch {chapter_index:03d}) has {non_ws_count} chars (> {CHAR_EARLY_CHAPTER_MAX}). Early chapters must be compact (2,200~2,800 chars) to maximize reader completion rate.")

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

    # Body text first line header check (prevent double title rendering)
    if RE_BODY_FIRST_LINE_HEADER.search(first_non_empty_line):
        issues.append(f"Body text first line contains title header ('{first_non_empty_line[:30]}...'). Body text must start directly with novel opening paragraph to prevent double title rendering in App.")

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

    # Microscopic AI slop phrases (Recommendation Traffic Risk)
    micro_slop_matches = [m.group(0) for m in RE_MICRO_AI_SLOP.finditer(text)]
    if micro_slop_matches:
        warnings.append(f"Microscopic AI slop phrases detected ({len(micro_slop_matches)} instances, e.g. '{micro_slop_matches[0]}').")

    # Omniscient protagonist clichés (Gary Stu / Flat narrative risk without real stakes)
    omni_matches = [m.group(0) for m in RE_OMNISCIENT_PROTAGONIST.finditer(text)]
    if len(omni_matches) >= 2:
        warnings.append(f"High frequency of omniscient protagonist clichés ({len(omni_matches)} instances, e.g. '{omni_matches[0]}'). Narrative risks Gary Stu syndrome with no vulnerability or real stakes.")

    # Modern macro/corporate financial jargon clash
    macro_matches = [m.group(0) for m in RE_GENRE_CLASH_MACRO.finditer(text)]
    if macro_matches:
        warnings.append(f"Modern macroeconomic/corporate jargon detected ({len(macro_matches)} instances, e.g. '{macro_matches[0]}'). Severe risk of genre clash between traditional setting and dry business treatise.")

    # Burstiness & Paragraph Variance check
    paragraphs = [p for p in text.splitlines() if p.strip()]
    if len(paragraphs) >= 12:
        mean_p, std_p, short_p = calculate_burstiness(paragraphs)
        if std_p < 14.0 and short_p == 0:
            warnings.append(f"Low paragraph burstiness (std_dev={std_p:.1f}, 0 short punchlines, high AI rhythmic uniformity).")

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
    parser = argparse.ArgumentParser(description="Audit novel files for Fanqie signing & recommendation review standards.")
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
    print(f" FANQIE SIGNING & RECOMMENDATION AUDIT TOOL")
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
        print("\nResult: SUCCESS - All chapters meet Fanqie signing & recommendation criteria.\n")
        sys.exit(0)

if __name__ == '__main__':
    main()
