# expense-tracker

Tiny command line expense tracker (Python 3, standard library only).

## Usage

    python -m expense_tracker.cli add 12.5 food --desc lunch
    python -m expense_tracker.cli total
    python -m expense_tracker.cli categories
    python -m expense_tracker.cli report --format csv
    python -m expense_tracker.cli export json out.json

## Tests

    python -m unittest discover -v

## Input rules
`amount` must be a finite number greater than 0 and `category` must not be blank; otherwise
`add` prints `error: ...` to stderr and exits with code 2 (nothing is saved). CSV output is
RFC 4180-quoted and text starting with `= + - @` is prefixed with `'` to avoid spreadsheet formulas.
