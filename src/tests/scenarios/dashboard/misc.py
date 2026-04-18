"""Dashboard login tests (misc)."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.dashboard_login import (
    click_back_to_igoristan_link,
    open_dashboard_login_page,
    verify_dashboard_login_page,
)
from lib.ext.ocarina.adapters.selenium.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.dashboard.login import DashboardLoginPage
from tests.scenarios.homepage.verify_homepage import verify_homepage

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def just_go_back_to_igoristan(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardLoginPage]]:
    """Verify the 'go back to Igoristan' link."""
    on_dashboard_login_page = DashboardLoginPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_dashboard_login_page, open_dashboard_login_page)
            .failure(just_log_error("Failed to open the dashboard login page..."))
            .success(just_log_success("Opened the dashboard login page!")),
            act(on_dashboard_login_page, verify_dashboard_login_page)
            .failure(
                just_log_error(
                    "Failed to verify the dashboard login page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the dashboard login page!"
                )
            ),
            act(
                on_dashboard_login_page,
                click_back_to_igoristan_link,
            )
            .failure(
                just_log_error(
                    "Failed to click on the 'Back to Igoristan' link...",
                )
            )
            .success(just_log_success("Clicked the 'Back to Igoristan' link!")),
        ),
    ]


test_dashboard_login_page_back_to_igoristan_button = create_selenium_test(
    name="Use the go back to Igoristan button",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=just_go_back_to_igoristan(driver, logger)
    ),
    post_test_scenarios_fragments=[verify_homepage],
)
