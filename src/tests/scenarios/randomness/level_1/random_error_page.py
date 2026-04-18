"""Test that random error page can be loaded (flaky)."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.random_error_page import (
    open_random_error_page,
    verify_random_error_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.random_error import RandomErrorPage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def random_error_render(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[RandomErrorPage]]:
    """Verify that random error page reaches its first render."""
    on_random_error_page = RandomErrorPage(driver=driver)

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
            act(on_random_error_page, open_random_error_page)
            .failure(just_log_error("Failed to open the random error page..."))
            .success(just_log_success("Opened the random error page!")),
            act(on_random_error_page, verify_random_error_page)
            .failure(
                log_error_with_current_url(
                    "Failed to verify the random error page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the random error page!"
                )
            ),
        ),
    ]


test_random_error_page_render = create_selenium_test(
    name="Random error page render",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=random_error_render(driver, logger)
    ),
)
