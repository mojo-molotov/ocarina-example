"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.dashboard.protected_page import DashboardProtectedPage


def open_dashboard_protected_page(p: DashboardProtectedPage) -> DashboardProtectedPage:
    """Open the Dashboard welcome page."""
    return p.open()


def verify_dashboard_protected_page(
    p: DashboardProtectedPage,
) -> DashboardProtectedPage:
    """Verify we are on the Dashboard welcome page."""
    return p.verify()


def click_on_back_to_dashboard_btn(p: DashboardProtectedPage) -> DashboardProtectedPage:
    """Click on go to nested page btn."""
    return p.click_on_back_to_dashboard_btn()
