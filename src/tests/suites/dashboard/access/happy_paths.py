"""Igoristan login test suite (happy paths)."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.dashboard.access.happy_paths import (
    test_dashboard_login_with_otp_happy_path,
    test_dashboard_login_without_otp_happy_path,
)
from tests.scenarios.dashboard.back_to_igoristan import (
    test_dashboard_login_page_back_to_igoristan_button,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_login_happy_paths_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's login test suite (happy paths)."""
    return TestSuite(
        name="Login happy paths",
        tests=[
            test_dashboard_login_without_otp_happy_path,
            test_dashboard_login_with_otp_happy_path,
            test_dashboard_login_page_back_to_igoristan_button,
        ],
        drivers_pool=drivers_pool,
    )
