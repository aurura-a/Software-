"""Tests added for the two mitigated risks (R-02 input validation, R-03 CSV safety)."""
import contextlib
import csv
import io
import os
import tempfile
import unittest

from expense_tracker.cli import main
from expense_tracker.tracker import Tracker


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = os.path.join(self.dir.name, "e.json")


class TestR02Validation(BaseCase):
    def test_rejects_bad_amounts(self):
        for bad in (-5, 0, float("nan"), float("inf"), True, "10", None):
            with self.subTest(amount=bad):
                with self.assertRaises(ValueError):
                    Tracker(self.path).add(bad, "food")

    def test_rejects_blank_category(self):
        for bad in ("", "   ", None):
            with self.subTest(category=bad):
                with self.assertRaises(ValueError):
                    Tracker(self.path).add(10, bad)

    def test_rejected_add_changes_nothing(self):
        t = Tracker(self.path)
        with self.assertRaises(ValueError):
            t.add(-1, "food")
        self.assertEqual(t.items, [])
        self.assertFalse(os.path.exists(self.path))

    def test_valid_add_still_works(self):
        t = Tracker(self.path)
        t.add(12.5, " food ", "lunch")
        self.assertEqual(t.total(), 12.5)

    def test_cli_invalid_amount_exit_code(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(["--file", self.path, "add", "-5", "food"])
        self.assertEqual(code, 2)
        self.assertIn("error", err.getvalue())
        self.assertFalse(os.path.exists(self.path))

    def test_cli_nan_amount_rejected(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--file", self.path, "add", "nan", "food"]), 2)


class TestR03CsvSafety(BaseCase):
    def rows(self, tracker):
        return list(csv.reader(io.StringIO(tracker.report("csv"))))

    def test_comma_in_description_stays_one_cell(self):
        t = Tracker(self.path)
        t.add(5, "food", "lunch, with friends")
        self.assertEqual(self.rows(t)[1], ["5", "food", "lunch, with friends"])

    def test_formula_prefixes_are_neutralised(self):
        for prefix in ("=", "+", "-", "@"):
            with self.subTest(prefix=prefix):
                t = Tracker(os.path.join(self.dir.name, "f%s.json" % ord(prefix)))
                t.add(5, "food", prefix + "SUM(A1:A9)")
                cell = self.rows(t)[1][2]
                self.assertFalse(cell.startswith(prefix), cell)
                self.assertIn("SUM(A1:A9)", cell)

    def test_category_is_neutralised_too(self):
        t = Tracker(self.path)
        t.add(5, '=cmd|" /C calc"!A0', "x")
        self.assertFalse(self.rows(t)[1][1].startswith("="))

    def test_plain_text_unchanged(self):
        t = Tracker(self.path)
        t.add(10, "food", "lunch")
        self.assertEqual(self.rows(t)[1], ["10", "food", "lunch"])

    def test_export_file_matches_report(self):
        t = Tracker(self.path)
        t.add(5, "food", "a,b")
        out = os.path.join(self.dir.name, "o.csv")
        t.export("csv", out)
        with open(out, newline="") as f:
            self.assertEqual(list(csv.reader(f))[1], ["5", "food", "a,b"])


if __name__ == "__main__":
    unittest.main()
