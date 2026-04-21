"""Igoristan login test suite (data-driven)."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.dashboard.data_driven.multi_login import multi_login_tests

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_login_data_driven_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's login test suite (data-driven)."""
    return TestSuite(
        name="Login (data-driven PoC)",
        tests=[*multi_login_tests],
        drivers_pool=drivers_pool,
    )
