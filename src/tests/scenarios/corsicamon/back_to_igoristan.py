"""Go back to Igoristan on both Corsicamon main screen and on enter API key screen."""

from typing import TYPE_CHECKING

from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.corsicamon_enter_api_key import (
    click_back_to_igoristan_link,
    open_corsicamon_enter_api_key_page,
    verify_corsicamon_enter_api_key_page,
)
from lib.connectors.test_steps.actions.corsicamon_main import (
    click_back_to_igoristan_link as click_back_to_igoristan_link_on_main_screen,
)
from lib.ext.ocarina.adapters.selenium.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.corsicamon.enter_api_key import CorsicamonEnterApiKeyPage
from pages.corsicamon.main import CorsicamonPage
from tests.scenarios.corsicamon.enter_api_key import enter_api_key
from tests.scenarios.homepage.verify_homepage import verify_homepage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def go_back_to_igoristan_on_main_screen(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[CorsicamonPage]]:
    """Go back to Igoristan from main page."""
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
                click_back_to_igoristan_link_on_main_screen,
            )
            .failure(
                just_log_error("Failed to click on the 'go back to Igoristan' link...")
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Clicked on the 'go back to Igoristan' link!"
                )
            )
        )
    ]


def go_back_to_igoristan_on_enter_api_key_screen(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[CorsicamonEnterApiKeyPage]]:
    """Immediately go back to Igoristan."""
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
            act(
                on_corsicamon_enter_api_key_page,
                verify_corsicamon_enter_api_key_page,
            )
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
            act(on_corsicamon_enter_api_key_page, click_back_to_igoristan_link)
            .failure(
                just_log_error(
                    "Failed to click on the 'go back to Igoristan' link...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Clicked on the 'go back to Igoristan' link!",
                )
            ),
        ),
    ]


test_go_back_to_igoristan_on_enter_api_key_screen = create_selenium_test(
    name="Go back to Igoristan without entering the API key",
    test_scenario=go_back_to_igoristan_on_enter_api_key_screen,
    post_test_scenarios=[verify_homepage],
)

test_go_back_to_igoristan_on_main_screen = create_selenium_test(
    name="Enter the API key then go back to Igoristan",
    test_scenario=go_back_to_igoristan_on_main_screen,
    pre_test_scenarios=[enter_api_key],
    post_test_scenarios=[verify_homepage],
)
