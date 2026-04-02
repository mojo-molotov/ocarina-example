"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.dashboard.welcome_page import DashboardWelcomePage


def open_dashboard_welcome_page(p: DashboardWelcomePage) -> DashboardWelcomePage:
    """Open the Dashboard welcome page."""
    return p.open()


def verify_dashboard_welcome_page(p: DashboardWelcomePage) -> DashboardWelcomePage:
    """Verify we are on the Dashboard welcome page."""
    return p.verify()


def click_on_go_to_nested_page_btn(p: DashboardWelcomePage) -> DashboardWelcomePage:
    """Click on go to nested page btn."""
    return p.click_on_go_to_nested_page_btn()


def verify_missing_otp_msg_is_displayed(
    p: DashboardWelcomePage,
) -> DashboardWelcomePage:
    """Verify the missing OTP msg is displayed."""
    return p.verify_missing_otp_msg_is_displayed()
