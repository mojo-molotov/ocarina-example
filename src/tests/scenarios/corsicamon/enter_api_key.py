"""Corsicamon enter API key page."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.corsicamon_enter_api_key import (
    enter_api_key_with_retries,
    open_corsicamon_enter_api_key_page,
    verify_corsicamon_enter_api_key_page,
)
from lib.connectors.test_steps.actions.corsicamon_enter_api_key import (
    fail_to_enter_api_key as _fail_to_enter_api_key,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.corsicamon.enter_api_key import CorsicamonEnterApiKeyPage

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def enter_api_key(driver: WebDriver, logger: ILogger):
    """Enter the API key."""
    on_corsicamon_enter_api_key_page = CorsicamonEnterApiKeyPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_corsicamon_enter_api_key_page, open_corsicamon_enter_api_key_page)
            .failure(
                just_log_error("Failed to open the Corsicamon enter API key page...")
            )
            .success(just_log_success("Opened the Corsicamon enter API key page!")),
            act(on_corsicamon_enter_api_key_page, verify_corsicamon_enter_api_key_page)
            .failure(
                just_log_error(
                    "Failed to verify the Corsicamon enter API key page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the Corsicamon enter API key page!"
                )
            ),
            act(
                on_corsicamon_enter_api_key_page,
                enter_api_key_with_retries(retries=20, logger=logger),
            )
            .failure(
                just_log_error(
                    "Failed to enter the API key...",
                )
            )
            .success(just_log_success("Entered the API key!")),
        ),
    ]


def fail_to_enter_api_key(driver: WebDriver, logger: ILogger):
    """Fail to enter the API key."""
    on_corsicamon_enter_api_key_page = CorsicamonEnterApiKeyPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_corsicamon_enter_api_key_page, open_corsicamon_enter_api_key_page)
            .failure(
                just_log_error("Failed to open the Corsicamon enter API key page...")
            )
            .success(just_log_success("Opened the Corsicamon enter API key page!")),
            act(on_corsicamon_enter_api_key_page, verify_corsicamon_enter_api_key_page)
            .failure(
                just_log_error(
                    "Failed to verify the Corsicamon enter API key page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the Corsicamon enter API key page!"
                )
            ),
            act(
                on_corsicamon_enter_api_key_page,
                _fail_to_enter_api_key,
            )
            .failure(
                just_log_error(
                    "Failed to reach the invalid API key error message...",
                )
            )
            .success(just_log_success("Reached the invalid API key error message!")),
        ),
    ]


test_enter_api_key = create_selenium_test(
    name="Enter API key",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=enter_api_key(driver, logger)
    ),
)

test_fail_to_enter_api_key = create_selenium_test(
    name="Fail to enter API key",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=fail_to_enter_api_key(driver, logger)
    ),
)
