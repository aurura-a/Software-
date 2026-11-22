"""Output formats (Strategy pattern): one function per format, looked up by name."""
import csv
import io
import json


def format_text(items, total):
    """Plain-text report, one line per expense plus a total."""
    lines = ["%s: %s (%s)" % (i["category"], i["amount"], i["description"]) for i in items]
    lines.append("TOTAL: %s" % total)
    return "\n".join(lines)


_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _safe_cell(text):
    """Prefix a quote to text that spreadsheets would interpret as a formula (CSV injection)."""
    text = str(text)
    return "'" + text if text.startswith(_FORMULA_PREFIXES) else text


def format_csv(items, total):
    """CSV report with a header row; quoted per RFC 4180 and safe to open in spreadsheets."""
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(["amount", "category", "description"])
    for i in items:
        writer.writerow([i["amount"], _safe_cell(i["category"]), _safe_cell(i["description"])])
    return buf.getvalue().rstrip("\n")


def format_json(items, total):
    """JSON report containing the items and the total."""
    return json.dumps({"items": items, "total": total})


FORMATTERS = {"text": format_text, "csv": format_csv, "json": format_json}


def get_formatter(fmt):
    """Return the formatter for `fmt`; raise ValueError for unknown formats."""
    try:
        return FORMATTERS[fmt]
    except KeyError:
        raise ValueError("unknown format") from None
