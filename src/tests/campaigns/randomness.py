"""Igoristan's randomness test campaign."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_campaign import TestCampaign
from tests.suites.randomness import (
    create_igoristan_randomness_level_1_test_suite,
    create_igoristan_randomness_level_2_test_suite,
    create_igoristan_randomness_level_3_test_suite,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_randomness_campaign(
    *, drivers_pool: SeleniumWebDriversPool
) -> TestCampaign:
    """Igoristan's randomness test campaign."""
    return TestCampaign(
        name="Random pages",
        suites=[
            create_igoristan_randomness_level_1_test_suite(drivers_pool=drivers_pool),
            create_igoristan_randomness_level_2_test_suite(drivers_pool=drivers_pool),
            create_igoristan_randomness_level_3_test_suite(drivers_pool=drivers_pool),
        ],
    )
