"""Capture RegEx for error pages titles (3 digits prefix)."""

import re

ERROR_PAGE_REGEX = re.compile(r"^\d{3}(?!\d)")
