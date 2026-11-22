import json
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


class TestAcceptanceCriteria(BaseCase):
    def test_ac1_total(self):
        t = Tracker(self.path)
        t.add(10, "food")
        t.add(5, "bus")
        self.assertEqual(t.total(), 15)

    def test_ac2_by_category(self):
        t = Tracker(self.path)
        t.add(10, "food")
        t.add(5, "food")
        t.add(3, "bus")
        self.assertEqual(t.by_category(), {"food": 15, "bus": 3})

    def test_ac3_persistence(self):
        Tracker(self.path).add(7, "food", "lunch")
        t2 = Tracker(self.path)
        self.assertEqual(t2.total(), 7)
        self.assertEqual(t2.items[0]["description"], "lunch")

    def test_ac4_report_text_csv_json(self):
        t = Tracker(self.path)
        t.add(10, "food", "lunch")
        self.assertIn("TOTAL: 10", t.report("text"))
        self.assertEqual(
            t.report("csv").splitlines(),
            ["amount,category,description", "10,food,lunch"],
        )
        self.assertEqual(json.loads(t.report("json"))["total"], 10)

    def test_ac4_export_writes_file(self):
        t = Tracker(self.path)
        t.add(10, "food", "lunch")
        out = os.path.join(self.dir.name, "out.csv")
        t.export("csv", out)
        with open(out) as f:
            self.assertEqual(f.read().splitlines()[1], "10,food,lunch")

    def test_ac4_unknown_format(self):
        with self.assertRaises(ValueError):
            Tracker(self.path).report("xml")

    def test_ac5_cli_exit_codes(self):
        self.assertEqual(main(["--file", self.path, "add", "12.5", "food"]), 0)
        self.assertEqual(main(["--file", self.path, "total"]), 0)
        self.assertEqual(main(["--file", self.path, "report"]), 0)


if __name__ == "__main__":
    unittest.main()
