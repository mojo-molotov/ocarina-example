"""Igoristan sacred upload form happy paths test suite."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.sacred_upload.just_go_back_to_igoristan import (
    test_sacred_upload_just_go_back_to_igoristan,
)
from tests.scenarios.sacred_upload.upload_files import (
    test_sacred_upload_form_with_some_files,
    test_sacred_upload_form_with_some_files_passing_by_del_btn,
    test_sacred_upload_form_with_some_files_passing_by_sin_btn,
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
            test_sacred_upload_form_with_some_files,
            test_sacred_upload_form_with_some_files_passing_by_del_btn,
            test_sacred_upload_form_with_some_files_passing_by_sin_btn,
            test_sacred_upload_just_go_back_to_igoristan,
        ],
        drivers_pool=drivers_pool,
    )
