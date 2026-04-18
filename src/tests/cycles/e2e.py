"""e2e test cycle."""

from typing import TYPE_CHECKING

from ocarina.dsl.testing.oc_test_cycle import TestCycle

from tests.campaigns.corsicamon import (
    create_igoristan_corsicamon_campaign,
    create_igoristan_corsicamon_smoke_campaign,
)
from tests.campaigns.dashboard_login import create_igoristan_login_campaign
from tests.campaigns.global_smoke_tests import create_igoristan_global_smoke_campaign
from tests.campaigns.randomness import create_igoristan_randomness_campaign
from tests.campaigns.sacred_upload import create_igoristan_sacred_upload_campaign

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_e2e_test_cycle(drivers_pool: SeleniumWebDriversPool):
    """e2e test cycle."""
    return TestCycle(
        name="e2e",
        campaigns=[
            create_igoristan_login_campaign(drivers_pool=drivers_pool),
            create_igoristan_randomness_campaign(drivers_pool=drivers_pool),
            create_igoristan_sacred_upload_campaign(drivers_pool=drivers_pool),
            create_igoristan_corsicamon_campaign(drivers_pool=drivers_pool),
        ],
        smoke_tests_campaigns=[
            create_igoristan_global_smoke_campaign(drivers_pool=drivers_pool),
            create_igoristan_corsicamon_smoke_campaign(drivers_pool=drivers_pool),
        ],
    )
