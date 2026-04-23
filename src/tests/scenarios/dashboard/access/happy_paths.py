"""Dashboard login tests (happy paths)."""

from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from caches.l1 import in_memory_cache_with_30m_ttl
from caches.reserve_free_cache_key import reserve_free_cache_key
from lib.connectors.test_steps.actions.dashboard_login import (
    login_without_otp_and_with_retries,
    open_dashboard_login_page,
    start_to_login_with_otp_and_with_retries,
    type_otp_with_retries,
    verify_dashboard_login_page,
    verify_otp_screen,
)
from lib.connectors.test_steps.actions.dashboard_protected_page import (
    verify_dashboard_protected_page,
)
from lib.connectors.test_steps.actions.dashboard_welcome import (
    click_on_go_to_nested_page_btn,
    verify_dashboard_welcome_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters
from lib.ext.ocarina.adapters.selenium.cli_getters import get_max_workers
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.dashboard.login import DashboardLoginPage
from pages.dashboard.protected_page import DashboardProtectedPage
from pages.dashboard.welcome_page import DashboardWelcomePage

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def dashboard_login_without_otp_happy_path(driver: WebDriver, logger: ILogger):
    """Verify that we can connect without OTP."""
    dashboard_creds = create_env_getters().get_credentials("dashboard")

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

    return [
        drive_page(
            act(on_dashboard_login_page, open_dashboard_login_page)
            .failure(just_log_error("Failed to open the dashboard login page..."))
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
            .success(just_log_success("Connected to the dashboard!")),
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


def dashboard_login_with_otp_happy_path(driver: WebDriver, logger: ILogger):
    """Verify that we can connect without OTP."""
    dashboard_creds = create_env_getters().get_credentials("dashboard")

    on_dashboard_login_page = DashboardLoginPage(driver=driver)
    on_dashboard_welcome_page = DashboardWelcomePage(driver=driver)
    on_dashboard_protected_page = DashboardProtectedPage(driver=driver)

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

    cache = in_memory_cache_with_30m_ttl
    fresh_cache_key_for_username = reserve_free_cache_key(cache)
    fresh_cache_key_for_otp_send_button_click_date = reserve_free_cache_key(cache)

    return [
        drive_page(
            act(on_dashboard_login_page, open_dashboard_login_page)
            .failure(just_log_error("Failed to open the dashboard login page..."))
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
                start_to_login_with_otp_and_with_retries(
                    dashboard_creds,
                    retries_amount,
                    cache=cache,
                    logger=logger,
                    username_cache_key=fresh_cache_key_for_username,
                    otp_send_button_click_date_cache_key=fresh_cache_key_for_otp_send_button_click_date,
                ),
            )
            .failure(
                just_log_error(
                    "Failed to fill and confirm the login form with OTP...",
                )
            )
            .success(just_log_success("Filled and confirmed the login form with OTP!")),
            act(
                on_dashboard_login_page,
                verify_otp_screen,
            )
            .failure(
                just_log_error(
                    "Failed to verify the OTP screen...",
                )
            )
            .success(just_log_success("Verified the OTP screen!")),
            act(
                on_dashboard_login_page,
                type_otp_with_retries(
                    retries_amount,
                    cache=cache,
                    logger=logger,
                    username_cache_key=fresh_cache_key_for_username,
                    otp_send_button_click_date_cache_key=fresh_cache_key_for_otp_send_button_click_date,
                ),
            )
            .failure(
                just_log_error(
                    "Failed to confirm the OTP code...",
                )
            )
            .success(just_log_success("Confirmed the OTP code!")),
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
            act(on_dashboard_welcome_page, click_on_go_to_nested_page_btn)
            .failure(
                just_log_error("Failed to click on the go to nested page button..."),
            )
            .success(just_log_success("Clicked the go to nested page button!")),
        ),
        drive_page(
            act(on_dashboard_protected_page, verify_dashboard_protected_page)
            .failure(
                just_log_error(
                    "Failed to verify the dashboard protected page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the dashboard protected page!"
                )
            )
        ),
    ]


test_dashboard_login_without_otp_happy_path = create_selenium_test(
    name="Connect to the dashboard, without OTP",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_login_without_otp_happy_path(driver, logger)
    ),
)

test_dashboard_login_with_otp_happy_path = create_selenium_test(
    name="Connect to the dashboard, with OTP",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_login_with_otp_happy_path(driver, logger)
    ),
)
