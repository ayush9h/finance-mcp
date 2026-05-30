import re

ANNUAL_REPORT_PATTERNS = [
    r"\bannual\s*report\b",
    r"\bannual\s*reports\b",
    r"\bar\s*\d{4}\b",
    r"\bar[-_\s]?\d{4}\b",
    r"\bintegrated\s*report\b",
    r"\bfinancial\s*report\b",
    r"\bfinancial\s*statements\b",
    r"\bannual-results\b",
]

annual_report_regex = re.compile(
    "|".join(ANNUAL_REPORT_PATTERNS),
    re.IGNORECASE,
)
