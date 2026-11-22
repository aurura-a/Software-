# Acceptance criteria (must remain true after every change)

| ID | Criterion | Covered by test |
|----|-----------|-----------------|
| AC1 | Adding expenses and calling `total()` returns the arithmetic sum. | `test_ac1_total` |
| AC2 | `by_category()` returns the sum of amounts per category. | `test_ac2_by_category` |
| AC3 | Expenses persist to the JSON file and are reloaded by a new `Tracker`. | `test_ac3_persistence` |
| AC4 | `report()`/`export()` support `text`, `csv`, `json`; unknown format raises `ValueError`. | `test_ac4_*` |
| AC5 | The CLI returns exit code 0 for valid `add`, `total`, `report` commands. | `test_ac5_cli_exit_codes` |
