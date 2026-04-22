"""Madness -> CORS Errors page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class CorsPage(SeleniumTitleMixin, POMBase):
    """Is madness."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize POM."""
        self._driver = driver
        self._use_api_anyway_btn = (
            By.CSS_SELECTOR,
            'a[href="/igoristan/corsicamon"]',
        )

    def verify(self, *, timeout: float | None = None) -> CorsPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            def _h1_contains_cors_errors(driver: WebDriver) -> bool:
                try:
                    h1 = driver.find_element(By.TAG_NAME, "h1")
                    return "cors errors:" in h1.text.lower()
                except Exception:  # noqa: BLE001
                    return False

            WebDriverWait(self._driver, timeout).until(ec.title_contains("Madness"))
            WebDriverWait(self._driver, timeout).until(_h1_contains_cors_errors)
        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def click_use_api_anyway_btn(self) -> CorsPage:
        """Click on use API anyway btn."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._use_api_anyway_btn)
        ).click()
        return self
