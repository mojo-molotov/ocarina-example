"""Igoristan's dashboard protected page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.dashboard import DASHBOARD_PROTECTED_PAGE_URL
from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout
from lib.ext.selenium.pages.verify_elements_presence import verify_elements_presence

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class DashboardProtectedPage(SeleniumTitleMixin, POMBase):
    """Igoristan's dashboard protected page."""

    def __init__(
        self, *, driver: WebDriver, url: str = DASHBOARD_PROTECTED_PAGE_URL
    ) -> None:
        """Initialize dashboard protected POM."""
        self._driver = driver
        self._URL = url
        self._logout_btn = (
            By.CSS_SELECTOR,
            '[data-testid="logout-btn"]',
        )
        self._dashboard_home_link = (By.CSS_SELECTOR, 'a[href="/igoristan/dashboard"]')

    def open(self) -> DashboardProtectedPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> DashboardProtectedPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "Logout button": self._logout_btn,
                    "Go back to dashboard button": self._dashboard_home_link,
                },
                page_title="the Igoristan dashboard protected page",
                timeout=timeout,
            )

            WebDriverWait(self._driver, timeout).until(
                ec.title_contains("Dashboard secret feature")
            )

            WebDriverWait(self._driver, timeout).until(
                ec.text_to_be_present_in_element(
                    (By.TAG_NAME, "h1"),
                    "Nested Dashboard",
                )
            )
        except TimeoutException as exc:
            raise PageVerificationError from exc

        return self

    def click_on_back_to_dashboard_btn(self) -> DashboardProtectedPage:
        """Click on back to dashboard button."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._dashboard_home_link)
        ).click()
        return self
