"""Madness -> Matchers."""

from typing import TYPE_CHECKING, final

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class MadnessPageMatchers:
    """Is madness."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize helper."""
        self._driver = driver

    def is_bastia_page(self) -> bool:
        """Quickly verify is bastia page."""
        timeout = min(get_timeout(), 5)

        def _h1_contains_bastia(driver: WebDriver) -> bool:
            try:
                h1 = driver.find_element(By.TAG_NAME, "h1")
                return "this is bastia" in h1.text.lower()
            except Exception:  # noqa: BLE001
                return False

        try:
            WebDriverWait(self._driver, timeout).until(_h1_contains_bastia)
        except TimeoutException:
            return False
        return True

    def is_cors_page(self) -> bool:
        """Quickly verify is CORS page."""
        timeout = min(get_timeout(), 5)

        def _h1_contains_cors_errors(driver: WebDriver) -> bool:
            try:
                h1 = driver.find_element(By.TAG_NAME, "h1")
                return "cors errors:" in h1.text.lower()
            except Exception:  # noqa: BLE001
                return False

        try:
            WebDriverWait(self._driver, timeout).until(_h1_contains_cors_errors)
        except TimeoutException:
            return False
        return True
