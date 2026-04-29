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
