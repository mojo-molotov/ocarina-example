"""Igoristan's Corsicamon test campaigns."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_campaign import TestCampaign
from tests.suites.corsicamon.smoke_tests import (
    create_igoristan_corsicamon_smoke_tests_suite,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_corsicamon_smoke_campaign(
    *, drivers_pool: SeleniumWebDriversPool
) -> TestCampaign:
    """Igoristan's Corsicamon smoke tests campaign."""
    return TestCampaign(
        name="Corsicamon (smoke tests)",
        suites=[
            create_igoristan_corsicamon_smoke_tests_suite(drivers_pool=drivers_pool),
        ],
    )
