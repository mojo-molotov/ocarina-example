"""Madness page."""

from typing import TYPE_CHECKING, Never, final

from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase

from constants.pages.madness import MADNESS_PAGE_URL

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class MadnessPage(SeleniumTitleMixin, POMBase):
    """Is madness."""

    def __init__(self, *, driver: WebDriver, url: str = MADNESS_PAGE_URL) -> None:
        """Initialize POM."""
        self._driver = driver
        self._URL = url

    def open(self) -> MadnessPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> Never:
        """Verify function."""
        msg = "Verify is undecidable on this POM, use matchers."
        raise NotImplementedError(msg)
