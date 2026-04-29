"""Fresh logs lambda builders."""

from typing import TYPE_CHECKING

from ocarina.custom_errors.test_framework.driver_died import DriverDiedError
from ocarina.infra.selenium.driver_healthcheck import driver_healthcheck

from lib.ext.ocarina.adapters.selenium.screenshotter import take_screenshot

if TYPE_CHECKING:
    from collections.abc import Callable

    from ocarina.dsl.testing_with_railway.internals.action_chain import (
        FailureHandler,
        SuccHandler,
    )
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def _append_current_url_in_msg(msg: str, driver: WebDriver) -> str:
    try:
        driver_healthcheck(driver)
        extended_msg = f"{msg}\nCurrent URL: {driver.current_url}"
    except DriverDiedError:
        extended_msg = f"{msg}\nThe WebDriver is down, can't provide the current URL."

    return extended_msg


def create_just_log_error(*, logger: ILogger) -> Callable[[str], FailureHandler]:
    """Error logger."""
    return lambda msg: lambda exc: logger.error(msg, exc=exc)


def create_log_error_with_current_url(
    *, logger: ILogger, driver: WebDriver
) -> Callable[[str], FailureHandler]:
    """Error logger, with current URL appended."""

    def unwrapped(msg: str) -> FailureHandler:
        def _log_error_with_url_effect(exc: Exception) -> None:
            extended_msg = _append_current_url_in_msg(msg, driver)
            return create_just_log_error(logger=logger)(extended_msg)(exc)

        return _log_error_with_url_effect

    return unwrapped


def create_just_log_success(*, logger: ILogger) -> Callable[[str], SuccHandler]:
    """Success logger."""

    def unwrapped(msg: str) -> SuccHandler:
        def _log_effect() -> None:
            logger.success(msg)

        return _log_effect

    return unwrapped


def create_log_success_and_take_screenshot(
    *, logger: ILogger, driver: WebDriver
) -> Callable[[str], SuccHandler]:
    """Success logger, with take screenshot side effect."""

    def unwrapped(msg: str) -> SuccHandler:
        def _log_and_take_screenshot_effect() -> None:
            performed_dependent_effect = create_just_log_success(logger=logger)(msg)()
            take_screenshot(driver=driver, logger=logger, category="SUCCESS")
            return performed_dependent_effect

        return _log_and_take_screenshot_effect

    return unwrapped


def create_log_success_with_current_url_and_take_screenshot(
    *, logger: ILogger, driver: WebDriver
) -> Callable[[str], SuccHandler]:
    """Success logger, with take screenshot side effect, and current URL appended."""

    def unwrapped(msg: str) -> SuccHandler:
        def _log_success_with_url_and_take_screenshot_effect() -> None:
            return create_log_success_and_take_screenshot(logger=logger, driver=driver)(
                _append_current_url_in_msg(msg, driver)
            )()

        return _log_success_with_url_and_take_screenshot_effect

    return unwrapped
