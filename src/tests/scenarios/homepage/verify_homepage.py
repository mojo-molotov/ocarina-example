"""Test that random loaders page can be fully loaded."""

from typing import TYPE_CHECKING

from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.homepage import open_homepage
from lib.connectors.test_steps.actions.homepage import (
    verify_homepage as _verify_homepage,
)
from lib.ext.ocarina.adapters.selenium.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.homepage import Homepage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def _open_homepage(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[Homepage]]:
    """Open the homepage."""
    on_homepage = Homepage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)

    return [
        drive_page(
            act(on_homepage, open_homepage)
            .failure(just_log_error("Failed to open the homepage..."))
            .success(just_log_success("Opened the homepage!")),
        ),
    ]


def verify_homepage(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[Homepage]]:
    """Verify the homepage."""
    on_homepage = Homepage(driver=driver)

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
            act(on_homepage, _verify_homepage)
            .failure(
                log_error_with_current_url(
                    "Failed to verify the homepage...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the homepage!"
                )
            ),
        ),
    ]


test_homepage = create_selenium_test(
    name="Test homepage",
    test_scenario=verify_homepage,
    pre_test_scenarios=[_open_homepage],
)
