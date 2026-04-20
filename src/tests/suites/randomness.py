"""Igoristan random features test suite."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.chaotic_form.send_it import test_send_chaotic_form
from tests.scenarios.randomness.level_1.random_error_page import (
    test_random_error_page_render,
)
from tests.scenarios.randomness.level_1.random_loaders_page import (
    test_random_loaders_page_full_load_and_back_to_homepage,
)
from tests.scenarios.randomness.level_2.madness import test_madness_page_render

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_randomness_level_1_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's random features test suite (lvl1)."""
    return TestSuite(
        name="Level 1",
        tests=[
            test_random_error_page_render,
            test_random_loaders_page_full_load_and_back_to_homepage,
        ],
        drivers_pool=drivers_pool,
    )


def create_igoristan_randomness_level_2_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's random features test suite (lvl2)."""
    return TestSuite(
        name="Level 2",
        tests=[
            test_madness_page_render,
        ],
        drivers_pool=drivers_pool,
    )


def create_igoristan_randomness_level_3_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's random features test suite (lvl3)."""
    return TestSuite(
        name="Level 3",
        tests=[
            test_send_chaotic_form,
        ],
        drivers_pool=drivers_pool,
    )
