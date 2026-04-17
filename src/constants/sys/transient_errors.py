"""Transient errors tuple."""

from ocarina.custom_errors.test_framework.driver_died import DriverDiedError
from ocarina.custom_errors.test_framework.pages import PageVerificationError
from selenium.common import WebDriverException

from lib.custom_errors.http import HttpErrorPageReachedError
from lib.custom_errors.transient_error import TransientError

transient_errors = (
    HttpErrorPageReachedError,
    PageVerificationError,
    WebDriverException,
    DriverDiedError,
    TransientError,
)


_match_page_transient_errors_to_remove = {PageVerificationError}

match_page_transient_errors = tuple(
    e for e in transient_errors if e not in _match_page_transient_errors_to_remove
)
