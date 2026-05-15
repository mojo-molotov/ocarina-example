"""CLI getters, intended to be quickly changed if required."""

from typing import TYPE_CHECKING

from ocarina.opinionated.cli.selenium.cli_store_singleton import (
    SeleniumCliStoreSingleton,
)

if TYPE_CHECKING:
    from ocarina.custom_types.selenium.supported_browsers import (
        SupportedSeleniumBrowser,
    )
    from ocarina.opinionated.loggers.custom_types.supported_loggers import (
        SupportedLogger,
    )


def get_timeout() -> int:
    """Get timeout in seconds from CLI."""
    timeout: int = SeleniumCliStoreSingleton().get("wait_timeout")
    return timeout


def get_logger_mode() -> SupportedLogger:
    """Get logger mode from CLI."""
    logger_mode: SupportedLogger = SeleniumCliStoreSingleton().get("logger")
    return logger_mode


def get_max_workers() -> int:
    """Get max workers amount from CLI."""
    max_workers: int = SeleniumCliStoreSingleton().get("workers")
    return max_workers


def get_only() -> list[str]:
    """Get only test ids from CLI."""
    only: list[str] = SeleniumCliStoreSingleton().get("only")
    return only


def get_exclude() -> list[str]:
    """Get excluded test ids from CLI."""
    exclude: list[str] = SeleniumCliStoreSingleton().get("exclude")
    return exclude


def get_browser() -> SupportedSeleniumBrowser:
    """Get browser from CLI."""
    browser: SupportedSeleniumBrowser = SeleniumCliStoreSingleton().get("browser")
    return browser


def get_driver_path() -> str:
    """Get driver path from CLI."""
    driver_path: str = SeleniumCliStoreSingleton().get("driver_path")
    return driver_path


def get_headless() -> bool:
    """Get headless flag from CLI."""
    headless: bool = SeleniumCliStoreSingleton().get("headless")
    return headless


def get_profile_path() -> str | None:
    """Get browser profile path from CLI (None when --profile-path is omitted)."""
    profile_path: str | None = SeleniumCliStoreSingleton().get("profile_path")
    return profile_path
