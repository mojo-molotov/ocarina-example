"""Igoristan's random error page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.random_error_page import RANDOM_ERROR_PAGE_URL
from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class RandomErrorPage(SeleniumTitleMixin, POMBase):
    """Igoristan's random error page."""

    def __init__(self, *, driver: WebDriver, url: str = RANDOM_ERROR_PAGE_URL) -> None:
        """Initialize random error POM."""
        self._driver = driver
        self._URL = url

    def open(self) -> RandomErrorPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> RandomErrorPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            expected_title_needle = "-404-"

            WebDriverWait(self._driver, timeout).until(
                ec.title_contains(expected_title_needle)
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self
