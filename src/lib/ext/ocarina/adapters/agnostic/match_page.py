"""Adapter for match_page."""

from ocarina.dsl.testing_with_railway.match_page import create_match_page

from constants.sys.transient_errors import transient_errors

match_page = create_match_page(raised_exceptions=transient_errors)
