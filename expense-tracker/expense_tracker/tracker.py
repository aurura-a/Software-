import json
import math
import os

from expense_tracker.formatters import get_formatter


class Tracker:
    def __init__(self, path="expenses.json"):
        self.path = path
        self.items = []
        if os.path.exists(path):
            with open(path) as f:
                self.items = json.load(f)

    def add(self, amount, category, description=""):
        """Validate and store one expense; raise ValueError (nothing is stored) if invalid."""
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("amount must be a number")
        if not math.isfinite(amount) or amount <= 0:
            raise ValueError("amount must be a finite number greater than 0")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("category must be a non-empty string")
        if not isinstance(description, str):
            raise ValueError("description must be a string")
        category = category.strip()
        self.items.append(
            {"amount": amount, "category": category, "description": description}
        )
        with open(self.path, "w") as f:
            json.dump(self.items, f)

    def total(self):
        t = 0
        for i in self.items:
            t = t + i["amount"]
        return t

    def by_category(self):
        res = {}
        for i in self.items:
            res[i["category"]] = res.get(i["category"], 0) + i["amount"]
        return res

    def report(self, fmt="text"):
        return get_formatter(fmt)(self.items, self.total())

    def export(self, fmt, out_path):
        data = self.report(fmt)
        with open(out_path, "w") as f:
            f.write(data)
