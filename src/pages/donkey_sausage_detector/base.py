"""Igoristan's donkey sausage eater detector page."""

from typing import TYPE_CHECKING, Never, final

from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase

from constants.pages.donkey_sausage_eater_detector import (
    DONKEY_SAUSAGE_EATER_DETECTOR_URL,
)

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class DonkeySausageEaterDetectorPage(SeleniumTitleMixin, POMBase):
    """Igoristan's donkey sausage eater detector page."""

    def __init__(
        self, *, driver: WebDriver, url: str = DONKEY_SAUSAGE_EATER_DETECTOR_URL
    ) -> None:
        """Initialize donkey sausage detector POM."""
        self._driver = driver
        self._URL = url

    def open(self) -> DonkeySausageEaterDetectorPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> Never:
        """Verify function."""
        msg = "Verify is undecidable on this POM, use matchers."
        raise NotImplementedError(msg)
