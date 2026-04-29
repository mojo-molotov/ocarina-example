"""Igoristan login test suite (unhappy paths)."""

from typing import TYPE_CHECKING

from lib.ext.ocarina.adapters.selenium.test_suite import TestSuite
from tests.scenarios.dashboard.access.unhappy_paths import (
    test_cant_access_any_dashboard_page_without_login,
    test_cant_access_the_protected_page_without_otp_using_the_ui,
    test_cant_access_the_protected_page_without_otp_using_the_url,
    test_login_attempt_with_invalid_pair_shows_an_error_message,
    test_login_page_doesnt_change_when_pushing_empty_login_form,
    test_login_page_doesnt_change_when_pushing_login_form_without_password,
    test_login_page_doesnt_change_when_pushing_login_form_without_username,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.web_drivers_pool import SeleniumWebDriversPool


def create_igoristan_login_unhappy_paths_test_suite(
    *,
    drivers_pool: SeleniumWebDriversPool,
) -> TestSuite:
    """Create the Igoristan's login test suite (unhappy paths)."""
    return TestSuite(
        name="Login unhappy paths",
        tests=[
            test_login_page_doesnt_change_when_pushing_empty_login_form,
            test_login_page_doesnt_change_when_pushing_login_form_without_username,
            test_login_page_doesnt_change_when_pushing_login_form_without_password,
            test_login_attempt_with_invalid_pair_shows_an_error_message,
            test_cant_access_the_protected_page_without_otp_using_the_ui,
            test_cant_access_the_protected_page_without_otp_using_the_url,
            test_cant_access_any_dashboard_page_without_login,
        ],
        drivers_pool=drivers_pool,
    )
