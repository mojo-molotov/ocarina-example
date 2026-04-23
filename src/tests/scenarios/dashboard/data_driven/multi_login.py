"""Login using a dataset."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.dashboard_login import (
    login_without_otp_and_with_retries,
    open_dashboard_login_page,
    verify_dashboard_login_page,
)
from lib.connectors.test_steps.actions.dashboard_welcome import (
    verify_dashboard_welcome_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.cli_getters import get_max_workers
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.dashboard.login import DashboardLoginPage
from pages.dashboard.welcome_page import DashboardWelcomePage
from tests.scenarios.dashboard.data_driven.datasets.multi_login import (
    multi_login_dataset,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.oc_test_scenario import SeleniumTestScenario
    from ocarina.opinionated.infra.env import (
        ImmutableCredentials,
    )
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def _create_login_scenario(credentials: ImmutableCredentials) -> SeleniumTestScenario:
    """Welcome to functional factories."""

    def _scenario(driver: WebDriver, logger: ILogger):  # noqa: ANN202
        dashboard_creds = credentials

        on_dashboard_login_page = DashboardLoginPage(driver=driver)
        on_dashboard_welcome_page = DashboardWelcomePage(driver=driver)

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

        retries_amount = max(get_max_workers(), 10)

        return Scenario(
            test_chain=[
                drive_page(
                    act(on_dashboard_login_page, open_dashboard_login_page)
                    .failure(
                        just_log_error("Failed to open the dashboard login page...")
                    )
                    .success(just_log_success("Opened the dashboard login page!")),
                    act(on_dashboard_login_page, verify_dashboard_login_page)
                    .failure(
                        log_error_with_current_url(
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
                        login_without_otp_and_with_retries(
                            dashboard_creds,
                            retries_amount,
                            logger=logger,
                        ),
                    )
                    .failure(
                        just_log_error(
                            "Failed to connect to the dashboard without OTP...",
                        )
                    )
                    .success(
                        just_log_success(
                            f"Connected to the dashboard as {dashboard_creds['login']}!"
                        )
                    ),
                ),
                drive_page(
                    act(on_dashboard_welcome_page, verify_dashboard_welcome_page)
                    .failure(
                        log_error_with_current_url(
                            "Failed to verify the dashboard welcome page...",
                        )
                    )
                    .success(
                        log_success_with_current_url_and_take_screenshot(
                            "Verified the dashboard welcome page!"
                        )
                    ),
                ),
            ]
        )

    return _scenario


multi_login_tests = [
    create_selenium_test(
        name=f"Login - {creds['login']}",
        test_scenario=_create_login_scenario(creds),
    )
    for creds in multi_login_dataset
]
