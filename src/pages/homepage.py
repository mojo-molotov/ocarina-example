"""Igoristan's homepage."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError

# ruff: noqa: S101
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.homepage import HOMEPAGE_URL
from lib.ext.ocarina.adapters.agnostic.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class Homepage(SeleniumTitleMixin, POMBase):
    """Igoristan's homepage."""

    def __init__(self, *, driver: WebDriver, url: str = HOMEPAGE_URL) -> None:
        """Initialize homepage POM."""
        self._driver = driver
        self._URL = url

    def open(self) -> Homepage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> Homepage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            expected_title = "Igoristan"

            WebDriverWait(self._driver, timeout).until(ec.title_is(expected_title))

            h1 = WebDriverWait(self._driver, timeout).until(
                ec.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            assert h1.text.lower() == expected_title.lower(), (
                f"Unexpected h1 text: '{h1.text}'"
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self
