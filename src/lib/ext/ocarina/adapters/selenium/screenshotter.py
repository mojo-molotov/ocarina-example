"""Screnshotter functions."""

from typing import TYPE_CHECKING, Literal

from ocarina.infra.selenium.create_screenshotter import create_selenium_screenshotter

if TYPE_CHECKING:
    from ocarina.custom_types.effect import Effect
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver

_Category = Literal["SUCCESS", "FAIL", "WARNING"]


def take_screenshot(*, driver: WebDriver, logger: ILogger, category: _Category) -> None:
    """Take a screenshot (standardized prefixes)."""
    take_screenshot_dispatchers: dict[_Category, Effect] = {
        "FAIL": lambda: create_selenium_screenshotter(driver, logger).take_screenshot(
            prefix="FAIL", shots=3, burst_delay=0.5
        ),
        "SUCCESS": lambda: create_selenium_screenshotter(
            driver, logger
        ).take_screenshot(prefix="SUCCESS"),
        "WARNING": lambda: create_selenium_screenshotter(
            driver, logger
        ).take_screenshot(prefix="WARNING"),
    }

    take_screenshot_dispatchers[category]()


def take_screenshot_unstrict(driver: WebDriver, logger: ILogger, prefix: str) -> None:
    """Take a screenshot (free prefix)."""
    create_selenium_screenshotter(driver, logger).take_screenshot(prefix=prefix)
