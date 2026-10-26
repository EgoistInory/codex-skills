import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_fanqie_quality.py"
SPEC = importlib.util.spec_from_file_location("audit_fanqie_quality", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class ManuscriptScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def chapter(self, text, name="001-章名.md"):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def cli(self, *args):
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), *map(str, args)],
            capture_output=True, encoding="utf-8", env=env,
            timeout=15,
        )

    def test_normal_chinese_book_marks_are_not_blocking(self):
        path = self.chapter("她合上《本草纲目》，推开药铺的门。", "001-读《本草》.md")
        result = AUDIT.audit_file(str(path), min_chars=0)
        self.assertEqual(result["issues"], [])
        self.assertNotEqual(result["status"], "FAIL")

    def test_short_chapter_is_a_configurable_review_hint(self):
        path = self.chapter("门开了。")
        default = AUDIT.audit_file(str(path))
        configured = AUDIT.audit_file(str(path), min_chars=0)
        self.assertEqual(default["issues"], [])
        self.assertTrue(any("configured minimum" in w for w in default["warnings"]))
        self.assertFalse(any("configured minimum" in w for w in configured["warnings"]))

    def test_source_title_convention_is_opt_in(self):
        path = self.chapter("第1章 推门\n\n门开了。")
        self.assertEqual(AUDIT.audit_file(str(path))["issues"], [])
        self.assertTrue(AUDIT.audit_file(str(path), body_only=True)["issues"])

    def test_modern_terms_only_trigger_historical_review_when_requested(self):
        path = self.chapter("她核对资金池，准备对冲风险。")
        modern = AUDIT.audit_file(str(path), min_chars=0)
        historical = AUDIT.audit_file(str(path), min_chars=0, historical=True)
        self.assertFalse(any("Historical-register" in w for w in modern["warnings"]))
        self.assertTrue(any("Historical-register" in w for w in historical["warnings"]))
        self.assertEqual(historical["issues"], [])

    def test_markdown_is_still_a_blocking_format_error(self):
        path = self.chapter("# 章名\n\n**门开了。**")
        self.assertEqual(AUDIT.audit_file(str(path))["status"], "FAIL")
        self.assertEqual(self.cli("--file", path).returncode, 1)

    def test_invalid_utf8_is_still_a_blocking_error(self):
        path = self.root / "001-broken.txt"
        path.write_bytes(b"\xff\xfe\x00")
        self.assertEqual(AUDIT.audit_file(str(path))["status"], "FAIL")
        self.assertEqual(self.cli("--file", path).returncode, 1)

    def test_crlf_is_a_review_hint_not_a_platform_failure(self):
        path = self.root / "001-lines.txt"
        path.write_bytes("门开了。\r\n她没有回头。\r\n".encode("utf-8"))
        result = AUDIT.audit_file(str(path), min_chars=0)
        self.assertEqual(result["issues"], [])
        self.assertTrue(any("CRLF" in w for w in result["warnings"]))

    def test_warning_exit_codes_and_read_only_behavior(self):
        path = self.chapter("门开了。")
        before = path.read_bytes()
        normal = self.cli("--file", path, "--min-chars", "0")
        strict = self.cli("--file", path, "--min-chars", "0", "--strict")
        self.assertEqual(normal.returncode, 0, normal.stderr)
        self.assertEqual(strict.returncode, 1, strict.stderr)
        self.assertIn("Warnings", normal.stdout)
        self.assertEqual(path.read_bytes(), before)

    def test_empty_or_invalid_targets_fail(self):
        self.assertEqual(self.cli("--dir", self.root).returncode, 1)
        self.assertEqual(self.cli("--file", self.root / "missing.txt").returncode, 1)
        self.assertEqual(self.cli("--dir", self.root, "--file", "other.txt").returncode, 2)
        self.assertEqual(self.cli("--dir", self.root, "--min-chars", "-1").returncode, 2)


if __name__ == "__main__":
    unittest.main()
