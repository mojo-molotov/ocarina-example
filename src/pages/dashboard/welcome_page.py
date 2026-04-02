"""Igoristan's dashboard welcome page."""

from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError

# ruff: noqa: S101
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.dashboard import DASHBOARD_URL
from lib.ext.ocarina.adapters.agnostic.cli_getters import get_timeout
from lib.ext.selenium.pages.verify_elements_presence import verify_elements_presence

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class DashboardWelcomePage(SeleniumTitleMixin, POMBase):
    """Igoristan's dashboard welcome page."""

    def __init__(self, *, driver: WebDriver, url: str = DASHBOARD_URL) -> None:
        """Initialize dashboard welcome POM."""
        self._driver = driver
        self._URL = url
        self._logout_btn = (
            By.CSS_SELECTOR,
            '[data-testid="logout-btn"]',
        )
        self._dashboard_protected_page_link = (
            By.CSS_SELECTOR,
            '[data-testid="go-to-nested-page-btn"]',
        )
        self._missing_otp_msg = (
            By.XPATH,
            "//*[contains(text(), 'requires OTP authentication')]",
        )

    def open(self) -> DashboardWelcomePage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> DashboardWelcomePage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "Logout button": self._logout_btn,
                    "Go to nested page button": self._dashboard_protected_page_link,
                },
                page_title="the Igoristan dashboard welcome page",
                timeout=timeout,
            )

            needle = "Dashboard"
            expected_h1 = "Dashboard"

            WebDriverWait(self._driver, timeout).until(ec.title_contains(needle))

            h1 = WebDriverWait(self._driver, timeout).until(
                ec.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            assert h1.text.lower() == expected_h1.lower(), (
                f"Unexpected h1 text: '{h1.text}'"
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def verify_missing_otp_msg_is_displayed(self) -> DashboardWelcomePage:
        """Verify the missing OTP msg is displayed."""
        try:
            timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "Missing OTP msg": self._missing_otp_msg,
                },
                timeout=timeout,
            )

        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def click_on_go_to_nested_page_btn(self) -> DashboardWelcomePage:
        """Click on go to nested page btn."""
        timeout = get_timeout()
        btn = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._dashboard_protected_page_link)
        )
        btn.click()
        return self
