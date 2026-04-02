"""Igoristan random features test suite."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.randomness.level_1.random_error_page import (
    test_random_error_page_render,
)
from tests.scenarios.randomness.level_1.random_loaders_page import (
    test_random_loaders_page_full_load_and_back_to_homepage,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_randomness_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's random features test suite."""
    return TestSuite(
        name="Level 1",
        tests=[
            test_random_error_page_render,
            test_random_loaders_page_full_load_and_back_to_homepage,
        ],
        drivers_pool=drivers_pool,
    )
