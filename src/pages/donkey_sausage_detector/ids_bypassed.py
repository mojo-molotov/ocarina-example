"""Igoristan's donkey sausage eater detector page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout
from lib.ext.selenium.pages.verify_elements_presence import verify_elements_presence

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class IDSBypassedPage(SeleniumTitleMixin, POMBase):
    """Igoristan's donkey sausage eater detector IDS bypassed page."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize donkey sausage detector (IDS bypassed) POM."""
        self._back_to_igoristan_link = (By.CSS_SELECTOR, 'a[href="/igoristan/"]')
        self._driver = driver

    def verify(self, *, timeout: float | None = None) -> IDSBypassedPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "Back to Igoristan link": self._back_to_igoristan_link,
                },
                page_title="the Igoristan DSED IDS bypassed page",
                timeout=timeout,
            )

            WebDriverWait(self._driver, timeout).until(
                ec.title_contains("The donkey sausage eater detector")
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self
