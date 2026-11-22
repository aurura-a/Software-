"""Re-run the baseline probes against the final code; expected outcomes are shown per probe."""
import csv, io, json, os, tempfile
from expense_tracker.tracker import Tracker

d = tempfile.mkdtemp()
def new(n): return Tracker(os.path.join(d, n))

print("--- P1 float money (NOT mitigated, residual risk R-01)")
t = new("p1.json"); t.add(0.1, "a"); t.add(0.2, "a"); print("total() =", repr(t.total()))

print("--- P2 validation (mitigated R-02)")
t = new("p2.json")
for amt, cat in ((-250, "x"), (0, "x"), (float("nan"), "x"), (float("inf"), "x"), (5, "")):
    try:
        t.add(amt, cat); print("ACCEPTED", amt, repr(cat))
    except ValueError as e:
        print("rejected %r %r -> %s" % (amt, cat, e))
print("items stored:", t.items, "| file created:", os.path.exists(t.path))

print("--- P3 CSV comma (mitigated)")
t = new("p3.json"); t.add(5, "food", "lunch, with friends")
print(repr(t.report("csv").splitlines()[1]), "->", next(csv.reader(io.StringIO(t.report("csv").splitlines()[1]))))

print("--- P4 CSV formula injection (mitigated R-03)")
t = new("p4.json"); t.add(5, "food", '=HYPERLINK("http://evil.example","click")')
print(t.report("csv").splitlines()[1])

print("--- P5 corrupted file (NOT mitigated, open risk R-05)")
p = os.path.join(d, "bad.json"); open(p, "w").write('[{"amount": 5, "categ')
try:
    Tracker(p)
except Exception as e:
    print("raised", type(e).__name__)
