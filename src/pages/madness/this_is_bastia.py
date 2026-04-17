"""Madness -> This is Bastia page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError

# ruff: noqa: S101
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.madness import MADNESS_PAGE_URL
from lib.ext.ocarina.adapters.agnostic.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class ThisIsBastiaPage(SeleniumTitleMixin, POMBase):
    """Is madness."""

    def __init__(self, *, driver: WebDriver, url: str = MADNESS_PAGE_URL) -> None:
        """Initialize POM."""
        self._driver = driver
        self._URL = url

    def open(self) -> ThisIsBastiaPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> ThisIsBastiaPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            expected_h1 = "This is bastia"
            title_needle = "Madness"

            WebDriverWait(self._driver, timeout).until(ec.title_contains(title_needle))

            h1 = WebDriverWait(self._driver, timeout).until(
                ec.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            assert h1.text.lower() == expected_h1.lower(), (
                f"Unexpected h1 text: '{h1.text}'"
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self
