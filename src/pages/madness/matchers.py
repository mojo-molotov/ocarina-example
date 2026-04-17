"""Madness -> Matchers."""

from typing import TYPE_CHECKING, final

from selenium.common.exceptions import StaleElementReferenceException

from pages.madness.cors import CorsPage
from pages.madness.this_is_bastia import ThisIsBastiaPage

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class MadnessPageMatchers:
    """Is madness."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize helper."""
        self._driver = driver

    def is_bastia_page(self) -> bool:
        """Verify is bastia page."""
        attempt = 0
        limit = 3

        while attempt < limit:  # noqa: PLR2004
            try:
                ThisIsBastiaPage(driver=self._driver).verify()
            except Exception:
                if (attempt + 1) > limit:
                    raise
            else:
                return True
            attempt += 1
        return False

    def is_cors_page(self) -> bool:
        """Verify is CORS page."""
        attempt = 0
        limit = 3

        while attempt < limit:  # noqa: PLR2004
            try:
                CorsPage(driver=self._driver).verify()
            except Exception:
                if (attempt + 1) > limit:
                    raise
            else:
                return True
            attempt += 1
        return False
