"""Igoristan Corsicamon happy paths test suite."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.corsicamon.add_corsicamon import test_add_corsicamon
from tests.scenarios.corsicamon.back_to_igoristan import (
    test_go_back_to_igoristan_on_enter_api_key_screen,
    test_go_back_to_igoristan_on_main_screen,
)
from tests.scenarios.corsicamon.new_draw import test_make_a_new_draw

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_corsicamon_happy_paths_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's Corsicamon happy paths test suite."""
    return TestSuite(
        name="Corsicamon happy paths",
        tests=[
            test_go_back_to_igoristan_on_enter_api_key_screen,
            test_go_back_to_igoristan_on_main_screen,
            test_add_corsicamon,
            test_make_a_new_draw,
        ],
        drivers_pool=drivers_pool,
    )
