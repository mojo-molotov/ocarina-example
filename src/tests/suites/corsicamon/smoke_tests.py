"""Corsicamon smoke tests suite."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.corsicamon.enter_api_key import (
    test_enter_api_key,
    test_fail_to_enter_api_key,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_corsicamon_smoke_tests_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Corsicamon smoke tests suite."""
    return TestSuite(
        name="API access",
        tests=[
            test_enter_api_key,
            test_fail_to_enter_api_key,
        ],
        drivers_pool=drivers_pool,
    )
