"""Dashboard login tests (unhappy paths)."""

from types import MappingProxyType
from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.dashboard_login import (
    login_without_otp,
    open_dashboard_login_page,
    verify_dashboard_login_page,
    verify_invalid_creds_msg_is_displayed,
)
from lib.connectors.test_steps.actions.dashboard_protected_page import (
    open_dashboard_protected_page,
)
from lib.connectors.test_steps.actions.dashboard_welcome import (
    click_on_go_to_nested_page_btn,
    verify_dashboard_welcome_page,
    verify_missing_otp_msg_is_displayed,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_just_log_success,
    create_log_error_with_current_url,
    create_log_success_with_current_url_and_take_screenshot,
)
from pages.dashboard.login import DashboardLoginPage
from pages.dashboard.protected_page import DashboardProtectedPage
from pages.dashboard.welcome_page import DashboardWelcomePage
from tests.scenarios.dashboard.access.happy_paths import (
    dashboard_login_without_otp_happy_path,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from ocarina.dsl.testing_with_railway.chain_actions import ChainRunner
    from ocarina.opinionated.infra.env import ImmutableCredentialsKeys
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def dashboard_login_empty_creds(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardLoginPage]]:
    """Verify the page doesn't change when pushing empty login form."""
    dashboard_creds: MappingProxyType[ImmutableCredentialsKeys, str] = MappingProxyType(
        {
            "login": "",
            "password": "",
        }
    )

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
                login_without_otp(dashboard_creds),
            )
            .failure(
                just_log_error(
                    "Failed to confirm login form...",
                )
            )
            .success(just_log_success("Confirmed empty login form!")),
        ),
    ] * 5


def dashboard_login_without_username(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardLoginPage]]:
    """Verify the page doesn't change when pushing login form without login."""
    dashboard_creds: MappingProxyType[ImmutableCredentialsKeys, str] = MappingProxyType(
        {
            "login": "",
            "password": create_env_getters().get_credentials("dashboard")["password"],
        }
    )

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
                login_without_otp(dashboard_creds),
            )
            .failure(
                just_log_error(
                    "Failed to confirm login form...",
                )
            )
            .success(just_log_success("Confirmed login form without login!")),
        ),
    ] * 5


def dashboard_login_without_password(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardLoginPage]]:
    """Verify the page doesn't change when pushing login form without login."""
    dashboard_creds: MappingProxyType[ImmutableCredentialsKeys, str] = MappingProxyType(
        {
            "login": create_env_getters().get_credentials("dashboard")["login"],
            "password": "",
        }
    )

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
                login_without_otp(dashboard_creds),
            )
            .failure(
                just_log_error(
                    "Failed to confirm login form...",
                )
            )
            .success(just_log_success("Confirmed login form without password!")),
        ),
    ] * 5


def dashboard_login_invalid_pair(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardLoginPage]]:
    """Verify the page display an error message when pushing invalid creds pair."""
    dashboard_creds: MappingProxyType[ImmutableCredentialsKeys, str] = MappingProxyType(
        {
            "login": "any",
            "password": "azerty123",
        }
    )

    on_dashboard_login_page = DashboardLoginPage(driver=driver)

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
                login_without_otp(dashboard_creds),
            )
            .failure(
                just_log_error(
                    "Failed to connect to the dashboard without OTP...",
                )
            )
            .success(just_log_success("Connected to the dashboard!")),
            act(on_dashboard_login_page, verify_invalid_creds_msg_is_displayed)
            .failure(
                just_log_error("Couldn't find the invalid creds error message....")
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Found the invalid creds error message!"
                )
            ),
        ),
    ]


def dashboard_access_to_protected_page_without_otp_using_the_ui(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardWelcomePage]]:
    """Verify the page display an error message when lacking OTP."""
    on_dashboard_welcome_page = DashboardWelcomePage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    just_log_success = create_just_log_success(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_dashboard_welcome_page, click_on_go_to_nested_page_btn)
            .failure(
                just_log_error("Failed to click on the go-to-nested-page button...")
            )
            .success(just_log_success("Clicked on the go-to-nested-page button!")),
            act(on_dashboard_welcome_page, verify_missing_otp_msg_is_displayed)
            .failure(
                just_log_error(
                    "Failed to find the missing OTP auth message...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Found the missing OTP auth message!"
                )
            ),
        ),
    ] * 5


def dashboard_access_to_protected_page_without_otp_using_the_url(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardProtectedPage] | ChainRunner[DashboardWelcomePage]]:
    """Verify the redirection."""
    on_dashboard_protected_page = DashboardProtectedPage(driver=driver)
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

    return [
        drive_page(
            act(on_dashboard_protected_page, open_dashboard_protected_page)
            .failure(just_log_error("Failed to open the dashboard protected page..."))
            .success(just_log_success("Entered dashboard protected page URL directly!"))
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
                    "Verified the dashboard welcome page: the user has been redirected!"
                )
            ),
        ),
    ] * 5


def dashboard_access_to_protected_page_without_login(
    driver: WebDriver, logger: ILogger
) -> Sequence[ChainRunner[DashboardProtectedPage] | ChainRunner[DashboardLoginPage]]:
    """Verify the redirection."""
    on_dashboard_protected_page = DashboardProtectedPage(driver=driver)
    on_dashboard_login_page = DashboardLoginPage(driver=driver)

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
            act(on_dashboard_protected_page, open_dashboard_protected_page)
            .failure(just_log_error("Failed to open the dashboard protected page..."))
            .success(just_log_success("Entered dashboard protected page URL directly!"))
        ),
        drive_page(
            act(on_dashboard_login_page, verify_dashboard_login_page)
            .failure(
                log_error_with_current_url(
                    "Failed to verify the dashboard login page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the dashboard login page: the user has been redirected!"
                )
            ),
        ),
    ] * 5


test_login_page_doesnt_change_when_pushing_empty_login_form = create_selenium_test(
    name="No page change when pushing empty form",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_login_empty_creds(driver, logger)
    ),
)

test_login_page_doesnt_change_when_pushing_login_form_without_username = (
    create_selenium_test(
        name="No page change when pushing login form without username",
        test_scenario=lambda driver, logger: Scenario(
            test_chain=dashboard_login_without_username(driver, logger)
        ),
    )
)

test_login_page_doesnt_change_when_pushing_login_form_without_password = (
    create_selenium_test(
        name="No page change when pushing login form without password",
        test_scenario=lambda driver, logger: Scenario(
            test_chain=dashboard_login_without_password(driver, logger)
        ),
    )
)

test_login_attempt_with_invalid_pair_shows_an_error_message = create_selenium_test(
    name="An error message is displayed on login fail",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_login_invalid_pair(driver, logger)
    ),
)

test_cant_access_the_protected_page_without_otp_using_the_ui = create_selenium_test(
    name="Can't access the protected page without OTP (using the UI)",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_access_to_protected_page_without_otp_using_the_ui(
            driver, logger
        )
    ),
    pre_test_scenarios_fragments=[dashboard_login_without_otp_happy_path],
)

test_cant_access_the_protected_page_without_otp_using_the_url = create_selenium_test(
    name="Can't access the protected page without OTP (using the URL)",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_access_to_protected_page_without_otp_using_the_url(
            driver, logger
        )
    ),
    pre_test_scenarios_fragments=[dashboard_login_without_otp_happy_path],
)

test_cant_access_any_dashboard_page_without_login = create_selenium_test(
    name="Can't access the protected page without login (using URL)",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=dashboard_access_to_protected_page_without_login(driver, logger)
    ),
)
