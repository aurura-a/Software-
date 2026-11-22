# Repository map (baseline)

| Item | Path | Notes |
|------|------|-------|
| Entry point | `expense_tracker/cli.py` (`python -m expense_tracker.cli`) | argparse, subcommands add/total/categories/report/export |
| Core module | `expense_tracker/tracker.py` | `Tracker`: load/save JSON, totals, `report()`, `export()` |
| Tests | `tests/test_tracker.py` | stdlib `unittest`, 7 tests |
| Dependencies | none | no `requirements.txt` / `pyproject.toml` |
| Build scripts | none | pure Python; `python3 -m compileall` used as a syntax check |
| Lint / type check | none configured | ruff/mypy/flake8 not installed in the audit environment |
| CI | none | no `.github/` |

Commands: run `python3 -m expense_tracker.cli ...`; test `python3 -m unittest discover -v`;
syntax/build check `python3 -m compileall -q expense_tracker tests`.
