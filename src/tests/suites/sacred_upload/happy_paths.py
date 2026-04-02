"""Igoristan sacred upload form happy paths test suite (WIP)."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.sacred_upload.upload_some_files import (
    test_sacred_upload_form_with_some_file_uploads,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_sacred_upload_happy_paths_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's sacred upload form happy paths test suite."""
    return TestSuite(
        name="Upload happy paths",
        tests=[
            test_sacred_upload_form_with_some_file_uploads,
        ],
        drivers_pool=drivers_pool,
    )
