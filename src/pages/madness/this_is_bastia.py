"""Madness -> This is Bastia page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class ThisIsBastiaPage(SeleniumTitleMixin, POMBase):
    """Is madness."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize POM."""
        self._driver = driver
        self._invader_detector_btn = (
            By.CSS_SELECTOR,
            'a[href="/igoristan/donkey-sausage-eater-detector"]',
        )

    def verify(self, *, timeout: float | None = None) -> ThisIsBastiaPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            def _h1_contains_bastia(driver: WebDriver) -> bool:
                try:
                    h1 = driver.find_element(By.TAG_NAME, "h1")
                    return "this is bastia" in h1.text.lower()
                except Exception:  # noqa: BLE001
                    return False

            WebDriverWait(self._driver, timeout).until(ec.title_contains("Madness"))
            WebDriverWait(self._driver, timeout).until(_h1_contains_bastia)
        except TimeoutException as exc:
            raise PageVerificationError from exc

        return self

    def click_invader_detector_btn(self) -> ThisIsBastiaPage:
        """Click on invader detector btn."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._invader_detector_btn)
        ).click()
        return self
