"""Adding a new Corsicamon feature on Corsicamon page."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.corsicamon_main import (
    enter_already_in_draw_corsicamon_id,
    enter_fresh_corsicamon_id_with_retries,
    enter_invalid_corsicamon_id,
    verify_corsicamon_main_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.corsicamon.main import CorsicamonPage
from tests.scenarios.corsicamon.enter_api_key import enter_api_key

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def try_to_add_corsicamon_using_invalid_id(driver: WebDriver, logger: ILogger):
    """Fail to add Corsicamon (invalid ID)."""
    on_corsicamon_page = CorsicamonPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_corsicamon_page, verify_corsicamon_main_page)
            .failure(just_log_error("Failed to verify the Corsicamon main page..."))
            .success(just_log_success("Verified the Corsicamon main page!")),
            act(on_corsicamon_page, enter_invalid_corsicamon_id)
            .failure(
                just_log_error(
                    "Failed to enter invalid Corsicamon ID...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Entered invalid Corsicamon ID!"
                )
            ),
        ),
    ]


def try_to_add_corsicamon_using_already_in_draw_id(driver: WebDriver, logger: ILogger):
    """Fail to add Corsicamon (already in draw ID)."""
    on_corsicamon_page = CorsicamonPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_corsicamon_page, verify_corsicamon_main_page)
            .failure(just_log_error("Failed to verify the Corsicamon main page..."))
            .success(just_log_success("Verified the Corsicamon main page!")),
            act(
                on_corsicamon_page,
                enter_already_in_draw_corsicamon_id,
            )
            .failure(
                just_log_error(
                    "Failed to enter already in draw Corsicamon ID...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Entered already in draw Corsicamon ID!"
                )
            ),
        ),
    ]


def add_corsicamon(driver: WebDriver, logger: ILogger):
    """Add Corsicamon."""
    on_corsicamon_page = CorsicamonPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_corsicamon_page, verify_corsicamon_main_page)
            .failure(just_log_error("Failed to verify the Corsicamon main page..."))
            .success(just_log_success("Verified the Corsicamon main page!")),
            act(
                on_corsicamon_page,
                enter_fresh_corsicamon_id_with_retries(logger=logger, retries=30),
            )
            .failure(
                just_log_error(
                    "Failed to add a Corsicamon...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot("Added a Corsicamon!")
            ),
        ),
    ]


test_try_to_add_corsicamon_using_already_in_draw_id = create_selenium_test(
    name="Fail to add Corsicamon (already in draw ID)",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=try_to_add_corsicamon_using_already_in_draw_id(driver, logger)
    ),
    pre_test_scenarios_fragments=[enter_api_key],
)

test_try_to_add_corsicamon_using_invalid_id = create_selenium_test(
    name="Fail to add Corsicamon (invalid ID)",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=try_to_add_corsicamon_using_invalid_id(driver, logger)
    ),
    pre_test_scenarios_fragments=[enter_api_key],
)

test_add_corsicamon = create_selenium_test(
    name="Add Corsicamon",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=add_corsicamon(driver, logger)
    ),
    pre_test_scenarios_fragments=[enter_api_key],
)
