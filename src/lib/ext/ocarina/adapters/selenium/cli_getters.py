"""CLI getters, intended to be quickly changed if required."""

from typing import TYPE_CHECKING

from ocarina.opinionated.cli.selenium.cli_store_singleton import (
    SeleniumCliStoreSingleton,
)

if TYPE_CHECKING:
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
