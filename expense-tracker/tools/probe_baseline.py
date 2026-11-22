import json, os, tempfile
from expense_tracker.tracker import Tracker

d = tempfile.mkdtemp()
def new(name="e.json"):
    return Tracker(os.path.join(d, name))

print("--- P1 float money: 0.1 + 0.2")
t = new("p1.json"); t.add(0.1, "a"); t.add(0.2, "a")
print("total() =", repr(t.total()))
print("report(json) =", t.report("json"))

print("--- P2 no validation: negative / zero / empty category / NaN")
t = new("p2.json")
t.add(100, "food"); t.add(-250, "refund?"); t.add(0, ""); t.add(float("nan"), "x")
print("total() =", repr(t.total()))
print("items =", t.items)

print("--- P3 CSV: comma in description breaks columns")
t = new("p3.json"); t.add(5, "food", "lunch, with friends")
row = t.report("csv").splitlines()[1]
print("row =", row, "| columns parsed by naive split:", len(row.split(",")), "(expected 3)")

print("--- P4 CSV formula injection")
t = new("p4.json"); t.add(5, "food", '=HYPERLINK("http://evil.example","click")')
print(t.report("csv").splitlines()[1])

print("--- P5 corrupted data file crashes constructor")
p = os.path.join(d, "bad.json")
open(p, "w").write('[{"amount": 5, "categ')
try:
    Tracker(p)
except Exception as e:
    print("raised", type(e).__name__, "-", e)

print("--- P6 duplicated format branches (static check)")
src = open("expense_tracker/tracker.py").read()
print('occurrences of \'"amount,category,description"\':', src.count('"amount,category,description"'))
print('occurrences of \'elif fmt == "csv"\' or \'if fmt == "csv"\':', src.count('fmt == "csv"'))
