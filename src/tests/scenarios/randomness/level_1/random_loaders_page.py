"""Test that random loaders page can be fully loaded."""

from typing import TYPE_CHECKING

from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.random_loaders import (
    click_back_to_igoristan_link,
    open_random_loaders_page,
    verify_full_load,
    verify_random_loaders_page,
)
from lib.ext.ocarina.adapters.selenium.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.random_loaders import RandomLoadersPage
from tests.scenarios.homepage.verify_homepage import verify_homepage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def _random_loaders_first_render(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[RandomLoadersPage]]:
    """Verify that random loaders page reaches its first render."""
    on_random_loaders_page = RandomLoadersPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_random_loaders_page, open_random_loaders_page)
            .failure(just_log_error("Failed to open the random loaders page..."))
            .success(just_log_success("Opened the random loaders page!")),
            act(on_random_loaders_page, verify_random_loaders_page)
            .failure(
                log_error_with_current_url(
                    "Failed to verify the random loaders page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the random loaders page!"
                )
            ),
        ),
    ]


def _random_loaders_full_load_happy_path(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[RandomLoadersPage]]:
    """Verify that random loaders page reaches its final state (fully loaded)."""
    on_random_loaders_page = RandomLoadersPage(driver=driver)

    log_error_with_current_url = create_log_error_with_current_url(
        logger=logger, driver=driver
    )
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_random_loaders_page, verify_full_load)
            .failure(
                log_error_with_current_url(
                    "Failed to verify that the page reaches its final state...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "All random elements loaded successfully!"
                )
            ),
        ),
    ]


def click_go_back_btn(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[RandomLoadersPage]]:
    """Click the go back button on the random loaders page."""
    on_random_loaders_page = RandomLoadersPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)

    return [
        drive_page(
            act(on_random_loaders_page, click_back_to_igoristan_link)
            .failure(
                just_log_error(
                    "Failed to click on the 'Back to Igoristan' button...",
                )
            )
            .success(just_log_success("Clicked on the 'Back to Igoristan' button!")),
        ),
    ]


test_random_loaders_page_full_load_and_back_to_homepage = create_selenium_test(
    name="Test Random Loaders page full load + click on the go back to Igoristan btn",
    test_scenario=click_go_back_btn,
    pre_test_scenarios=[
        _random_loaders_first_render,
        _random_loaders_full_load_happy_path,
    ],
    post_test_scenarios=[verify_homepage],
)
