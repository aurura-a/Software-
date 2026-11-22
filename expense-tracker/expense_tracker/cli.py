import argparse
import sys

from expense_tracker.tracker import Tracker


def main(argv=None):
    p = argparse.ArgumentParser(prog="expense-tracker")
    p.add_argument("--file", default="expenses.json")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("amount", type=float)
    a.add_argument("category")
    a.add_argument("--desc", default="")
    sub.add_parser("total")
    sub.add_parser("categories")
    r = sub.add_parser("report")
    r.add_argument("--format", default="text")
    e = sub.add_parser("export")
    e.add_argument("format")
    e.add_argument("out")
    args = p.parse_args(argv)

    t = Tracker(args.file)
    if args.cmd == "add":
        try:
            t.add(args.amount, args.category, args.desc)
        except ValueError as exc:
            print("error: %s" % exc, file=sys.stderr)
            return 2
        print("added")
    elif args.cmd == "total":
        print(t.total())
    elif args.cmd == "categories":
        for k, v in t.by_category().items():
            print("%s: %s" % (k, v))
    elif args.cmd == "report":
        print(t.report(args.format))
    elif args.cmd == "export":
        t.export(args.format, args.out)
        print("exported")
    return 0


if __name__ == "__main__":
    sys.exit(main())
