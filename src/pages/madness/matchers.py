"""Madness -> Matchers."""

from typing import TYPE_CHECKING, final

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from pages.madness.this_is_bastia import ThisIsBastiaPage

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class MadnessPageMatchers:
    """Is madness."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize helper."""
        self._driver = driver

    def is_bastia_page(self, *, timeout: float = 2.0) -> bool:
        """Quickly verify is bastia page."""
        WebDriverWait(self._driver, timeout).until(ec.title_contains("Madness"))
        h1 = self._driver.find_element(By.TAG_NAME, "h1")
        return "This is Bastia".lower() in h1.text.lower()

    def is_cors_page(self, *, timeout: float = 2.0) -> bool:
        """Quickly verify is CORS page."""
        WebDriverWait(self._driver, timeout).until(ec.title_contains("Madness"))
        h1 = self._driver.find_element(By.TAG_NAME, "h1")
        return "CORS Errors:".lower() in h1.text.lower()
