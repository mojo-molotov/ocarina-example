"""Igoristan's corsicamon enter API key page."""

import random
from contextlib import suppress
from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.dsl.invariants.assertions import (
    is_positive,
)
from ocarina.dsl.invariants.validate import validate
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.corsicamon import CORSICAMON_PAGE_URL
from lib.ext.ocarina.adapters.agnostic.cli_getters import get_timeout
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters
from lib.ext.ocarina.adapters.selenium.screenshotter import take_screenshot
from lib.ext.selenium.pages.verify_elements_presence import verify_elements_presence

if TYPE_CHECKING:
    from ocarina.custom_types.effect import Effect
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class CorsicamonEnterApiKeyPage(SeleniumTitleMixin, POMBase):
    """Igoristan's corsicamon enter API key page."""

    def __init__(self, *, driver: WebDriver, url: str = CORSICAMON_PAGE_URL) -> None:
        """Initialize dashboard login POM."""
        self._URL = url
        self._driver = driver

        self._api_key_input = (By.ID, "enter-api-key")
        self._igoristan_link = (By.CSS_SELECTOR, 'a[href="/igoristan/"]')
        self._access_corsicadex_btn = (
            By.CSS_SELECTOR,
            '[data-testid="access-corsicadex-btn"]',
        )
        self._corsicamon_network_error_container = (
            By.CSS_SELECTOR,
            '[data-testid="corsicadex-network-error"]',
        )
        self._corsicamon_network_error_retry_btn = (
            By.CSS_SELECTOR,
            '[data-testid="corsicadex-network-error-retry-btn"]',
        )

        timeout = get_timeout()

        self._confirm_api_key_dispatchers: dict[str, Effect] = {
            "focus_api_key_input_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._api_key_input))
                .send_keys(Keys.ENTER)
            ),
            "click_access_corsicamon_button": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._access_corsicadex_btn))
                .click()
            ),
            "focus_access_corsicamon_button_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._access_corsicadex_btn))
                .send_keys(Keys.ENTER)
            ),
        }

    def _get_random_confirm_api_key_dispatchers_key(self) -> str:
        return random.choice(  # noqa: S311
            list(self._confirm_api_key_dispatchers.keys())
        )

    def open(self) -> CorsicamonEnterApiKeyPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> CorsicamonEnterApiKeyPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "API key input": self._api_key_input,
                    "Back to Igoristan link": self._igoristan_link,
                    "Access Corsicadex button": self._access_corsicadex_btn,
                },
                page_title="Corsicamon enter API key page",
                timeout=timeout,
            )

            WebDriverWait(self._driver, timeout).until(ec.title_contains("Corsicamon"))

            WebDriverWait(self._driver, timeout).until(
                ec.text_to_be_present_in_element(
                    (By.TAG_NAME, "h1"),
                    "Enter API Key",
                )
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def click_retry_button(self) -> CorsicamonEnterApiKeyPage:
        """Click on the retry button."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._corsicamon_network_error_retry_btn)
        ).click()

        return self

    def click_back_to_igoristan_link(self) -> CorsicamonEnterApiKeyPage:
        """Click on the back to Igoristan link."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._igoristan_link)
        ).click()

        WebDriverWait(self._driver, timeout).until(
            ec.invisibility_of_element_located(self._igoristan_link)
        )

        return self

    def fail_to_enter_api_key(self) -> CorsicamonEnterApiKeyPage:
        """Fail to enter API key."""
        timeout = get_timeout()
        enter_api_key_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._api_key_input)
        )

        enter_api_key_input.clear()
        enter_api_key_input.send_keys(
            create_env_getters().get_value("igor_api_key") + "N-A-P-O-L-E-O-N"
        )

        self._confirm_api_key_dispatchers[
            self._get_random_confirm_api_key_dispatchers_key()
        ]()

        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._corsicamon_network_error_container)
        )
        return self

    def enter_api_key(self) -> CorsicamonEnterApiKeyPage:
        """Enter API key."""
        timeout = get_timeout()
        enter_api_key_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._api_key_input)
        )

        enter_api_key_input.clear()
        enter_api_key_input.send_keys(create_env_getters().get_value("igor_api_key"))

        self._confirm_api_key_dispatchers[
            self._get_random_confirm_api_key_dispatchers_key()
        ]()
        return self

    def enter_api_key_with_retries(
        self, *, retries: int, logger: ILogger
    ) -> CorsicamonEnterApiKeyPage:
        """Enter API key (n retries)."""
        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1
        self.enter_api_key()

        while attempts_count <= retries:
            timeout = get_timeout()
            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.invisibility_of_element_located(
                        self._corsicamon_network_error_container
                    )
                )
                break

            msg = (
                "Failed to enter the API Key."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            self.click_retry_button()
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = f"Entered the API Key. After {attempts_count} attempt{s}."

        logger.info(msg)
        return self
