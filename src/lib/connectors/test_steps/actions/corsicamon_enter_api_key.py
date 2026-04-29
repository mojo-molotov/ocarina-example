"""Functional connectors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from ocarina.ports.ilogger import ILogger

    from pages.corsicamon.enter_api_key import CorsicamonEnterApiKeyPage


def open_corsicamon_enter_api_key_page(
    p: CorsicamonEnterApiKeyPage,
) -> CorsicamonEnterApiKeyPage:
    """Open the Igoristan's Corsicamon enter API key page."""
    return p.open()


def verify_corsicamon_enter_api_key_page(
    p: CorsicamonEnterApiKeyPage,
) -> CorsicamonEnterApiKeyPage:
    """Verify we are on the Igoristan's Corsicamon enter API key page."""
    return p.verify()


def enter_api_key(
    p: CorsicamonEnterApiKeyPage,
) -> CorsicamonEnterApiKeyPage:
    """Enter the API key."""
    return p.enter_api_key()


def fail_to_enter_api_key(
    p: CorsicamonEnterApiKeyPage,
) -> CorsicamonEnterApiKeyPage:
    """Fail to enter the API key."""
    return p.fail_to_enter_api_key()


def click_back_to_igoristan_link(
    p: CorsicamonEnterApiKeyPage,
) -> CorsicamonEnterApiKeyPage:
    """Click on the back to Igoristan link."""
    return p.click_back_to_igoristan_link()


def click_retry_button(
    p: CorsicamonEnterApiKeyPage,
) -> CorsicamonEnterApiKeyPage:
    """Click on the retry button."""
    return p.click_retry_button()


def enter_api_key_with_retries(
    *,
    retries: int,
    logger: ILogger,
) -> Callable[[CorsicamonEnterApiKeyPage], CorsicamonEnterApiKeyPage]:
    """Click on the retry button."""

    def unwrapped(p: CorsicamonEnterApiKeyPage) -> CorsicamonEnterApiKeyPage:
        return p.enter_api_key_with_retries(retries=retries, logger=logger)

    return unwrapped
