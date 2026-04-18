"""Global smoke tests suite."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.homepage.verify_homepage import test_homepage

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_global_smoke_tests_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Global smoke tests suite."""
    return TestSuite(
        name="Global smoke tests",
        tests=[
            test_homepage,
        ],
        drivers_pool=drivers_pool,
    )
