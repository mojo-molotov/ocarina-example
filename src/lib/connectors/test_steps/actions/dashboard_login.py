"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from dogpile.cache import CacheRegion
    from ocarina.opinionated.infra.env import ImmutableCredentials
    from ocarina.ports.ilogger import ILogger

    from pages.dashboard.login import DashboardLoginPage


def open_dashboard_login_page(p: DashboardLoginPage) -> DashboardLoginPage:
    """Open the Dashboard login page."""
    return p.open()


def verify_dashboard_login_page(p: DashboardLoginPage) -> DashboardLoginPage:
    """Verify we are on the Igoristan's dashboard login page."""
    return p.verify()


def login_without_otp(
    creds: ImmutableCredentials,
) -> Callable[[DashboardLoginPage], DashboardLoginPage]:
    """Type creds and confirm input to connect to the dashboard, without OTP."""

    def unwrapped(p: DashboardLoginPage) -> DashboardLoginPage:
        return p.login_without_otp(creds)

    return unwrapped


def login_without_otp_and_with_retries(
    creds: ImmutableCredentials, retries: int, *, logger: ILogger
) -> Callable[[DashboardLoginPage], DashboardLoginPage]:
    """Type creds and confirm input to connect to the dashboard, without OTP."""

    def unwrapped(p: DashboardLoginPage) -> DashboardLoginPage:
        return p.login_without_otp_and_with_retries(creds, retries, logger=logger)

    return unwrapped


def start_to_login_with_otp(
    creds: ImmutableCredentials,
    *,
    username_cache_key: str,
    otp_send_button_click_date_cache_key: str,
    cache: CacheRegion,
) -> Callable[[DashboardLoginPage], DashboardLoginPage]:
    """Type creds and confirm input to connect to the dashboard, without OTP."""

    def unwrapped(p: DashboardLoginPage) -> DashboardLoginPage:
        return p.start_to_login_with_otp(
            creds,
            username_cache_key=username_cache_key,
            otp_send_button_click_date_cache_key=otp_send_button_click_date_cache_key,
            cache=cache,
        )

    return unwrapped


def start_to_login_with_otp_and_with_retries(  # noqa: PLR0913
    creds: ImmutableCredentials,
    retries: int,
    *,
    username_cache_key: str,
    otp_send_button_click_date_cache_key: str,
    logger: ILogger,
    cache: CacheRegion,
) -> Callable[[DashboardLoginPage], DashboardLoginPage]:
    """Enable OTP, fill fields and confirm to reach the OTP screen (n retries)."""

    def unwrapped(p: DashboardLoginPage) -> DashboardLoginPage:
        return p.start_to_login_with_otp_and_with_retries(
            creds,
            retries,
            username_cache_key=username_cache_key,
            otp_send_button_click_date_cache_key=otp_send_button_click_date_cache_key,
            logger=logger,
            cache=cache,
        )

    return unwrapped


def verify_otp_screen(p: DashboardLoginPage) -> DashboardLoginPage:
    """Verify the OTP screen."""
    return p.verify_otp_screen()


def type_otp(
    *,
    username_cache_key: str,
    otp_send_button_click_date_cache_key: str,
    logger: ILogger,
    cache: CacheRegion,
) -> Callable[[DashboardLoginPage], DashboardLoginPage]:
    """Type the OTP code but don't confirm it."""

    def unwrapped(p: DashboardLoginPage) -> DashboardLoginPage:
        return p.type_otp(
            username_cache_key=username_cache_key,
            otp_send_button_click_date_cache_key=otp_send_button_click_date_cache_key,
            logger=logger,
            cache=cache,
        )

    return unwrapped


def type_otp_with_retries(
    retries: int,
    *,
    username_cache_key: str,
    otp_send_button_click_date_cache_key: str,
    logger: ILogger,
    cache: CacheRegion,
) -> Callable[[DashboardLoginPage], DashboardLoginPage]:
    """Type the OTP code but don't confirm it."""

    def unwrapped(p: DashboardLoginPage) -> DashboardLoginPage:
        return p.type_otp_with_retries(
            retries,
            username_cache_key=username_cache_key,
            otp_send_button_click_date_cache_key=otp_send_button_click_date_cache_key,
            logger=logger,
            cache=cache,
        )

    return unwrapped


def verify_invalid_creds_msg_is_displayed(p: DashboardLoginPage) -> DashboardLoginPage:
    """Verify the invalid creds msg is displayed."""
    return p.verify_invalid_creds_msg_is_displayed()


def click_back_to_igoristan_link(p: DashboardLoginPage) -> DashboardLoginPage:
    """Click on the back to Igoristan link."""
    return p.click_back_to_igoristan_link()
