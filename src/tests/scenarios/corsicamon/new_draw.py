"""Making a new draw feature on Corsicamon page."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.corsicamon_main import (
    make_a_new_draw_with_retries,
    verify_enter_id_field_is_empty,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.corsicamon.main import CorsicamonPage
from tests.scenarios.corsicamon.add_corsicamon import (
    try_to_add_corsicamon_using_invalid_id,
)
from tests.scenarios.corsicamon.enter_api_key import enter_api_key

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def make_a_new_draw(driver: WebDriver, logger: ILogger):
    """Make a new draw."""
    on_corsicamon_page = CorsicamonPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(
                on_corsicamon_page,
                make_a_new_draw_with_retries(logger=logger, retries=10),
            )
            .failure(
                just_log_error(
                    "Failed to make a new draw...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot("Made a new draw!")
            ),
            act(on_corsicamon_page, verify_enter_id_field_is_empty)
            .failure(
                just_log_error(
                    "The 'Enter ID' field is not empty after this new draw...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "The 'Enter ID' field has been reset after this new draw!"
                )
            ),
        ),
    ]


test_make_a_new_draw = create_selenium_test(
    name="Make a new draw",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=make_a_new_draw(driver, logger)
    ),
    pre_test_scenarios_fragments=[
        enter_api_key,
        try_to_add_corsicamon_using_invalid_id,
    ],
)
