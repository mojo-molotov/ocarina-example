"""Igoristan's dashboard login page."""

import math
import random
import time
from contextlib import suppress
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.dsl.invariants.assertions import (
    is_iso_date_string,
    is_iso_utc_date_string,
    is_not_none,
    is_positive,
    is_str,
    is_truthy,
)
from ocarina.dsl.invariants.internals.validation_chain import chain_validations
from ocarina.dsl.invariants.validate import validate
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from api.retrieve_dashboard_otp_code import retrieve_dashboard_otp_code
from constants.pages.dashboard import DASHBOARD_URL
from constants.sys.redis_keys import OTP_SEND_LOCK_KEY
from lib.custom_errors.transient_error import TransientError
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters
from lib.ext.ocarina.adapters.selenium.cli_getters import get_max_workers, get_timeout
from lib.ext.ocarina.adapters.selenium.screenshotter import take_screenshot
from lib.ext.redis.client import get_redis_client
from lib.ext.selenium.pages.verify_elements_presence import verify_elements_presence

if TYPE_CHECKING:
    from dogpile.cache import CacheRegion
    from ocarina.custom_types.effect import Effect
    from ocarina.opinionated.infra.env import (
        ImmutableCredentials,
    )
    from ocarina.ports.ilogger import ILogger
    from redis.lock import Lock as RedisLock
    from selenium.webdriver.remote.webdriver import WebDriver

_PAGE_TITLE = "the Igoristan dashboard login page"


def _get_lock() -> RedisLock:
    client = get_redis_client()
    redis_lock: RedisLock = client.lock(OTP_SEND_LOCK_KEY, timeout=30)
    return redis_lock


@final
class DashboardLoginPage(SeleniumTitleMixin, POMBase):
    """Igoristan's dashboard login page."""

    def __init__(self, *, driver: WebDriver, url: str = DASHBOARD_URL) -> None:
        """Initialize dashboard login POM."""
        use_otp_checkbox_id = "use-otp"
        self._driver = driver
        self._URL = url
        self._username_input = (
            By.ID,
            "username",
        )
        self._password_input = (
            By.ID,
            "password",
        )
        self._igor_api_key_input = (By.ID, "otp-api-key")
        self._use_otp_checkbox = (
            By.ID,
            use_otp_checkbox_id,
        )
        self._use_otp_checkbox_label = (
            By.XPATH,
            f"//label[@for='{use_otp_checkbox_id}']",
        )
        self._login_btn = (
            By.CSS_SELECTOR,
            '[data-testid="login-btn"]',
        )
        self._back_to_igoristan_link = (By.CSS_SELECTOR, 'a[href="/igoristan/"]')

        self._confirm_otp_btn_on_otp_screen = (
            By.CSS_SELECTOR,
            '[data-testid="otp-btn"]',
        )
        self._otp_field_on_otp_screen = (
            By.ID,
            "otp-code",
        )
        self._invalid_credentials_msg = (
            By.XPATH,
            "//*[contains(text(), 'Invalid credentials.')]",
        )

        timeout = get_timeout()

        self._login_without_otp_action_dispatchers: dict[str, Effect] = {
            "focus_username_input_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._username_input))
                .send_keys(Keys.ENTER)
            ),
            "focus_password_input_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._password_input))
                .send_keys(Keys.ENTER)
            ),
            "click_login_button": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._login_btn))
                .click()
            ),
            "focus_login_button_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._login_btn))
                .send_keys(Keys.ENTER)
            ),
        }

        self._login_with_otp_action_dispatchers: dict[str, Effect] = {
            **self._login_without_otp_action_dispatchers,
            "focus_api_key_input_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._igor_api_key_input))
                .send_keys(Keys.ENTER)
            ),
        }

        self._confirm_otp_action_dispatchers: dict[str, Effect] = {
            "focus_otp_input_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._otp_field_on_otp_screen))
                .send_keys(Keys.ENTER)
            ),
            "click_otp_button": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(
                    ec.visibility_of_element_located(
                        self._confirm_otp_btn_on_otp_screen
                    )
                )
                .click()
            ),
            "focus_otp_button_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(
                    ec.visibility_of_element_located(
                        self._confirm_otp_btn_on_otp_screen
                    )
                )
                .send_keys(Keys.ENTER)
            ),
        }

    def _get_random_login_without_otp_action_key(self) -> str:
        return random.choice(  # noqa: S311
            list(self._login_without_otp_action_dispatchers.keys())
        )

    def _get_random_login_with_otp_action_key(self) -> str:
        return random.choice(  # noqa: S311
            list(self._login_with_otp_action_dispatchers.keys())
        )

    def _get_random_confirm_otp_action_key(self) -> str:
        return random.choice(  # noqa: S311
            list(self._confirm_otp_action_dispatchers.keys())
        )

    def open(self) -> DashboardLoginPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> DashboardLoginPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "Username input": self._username_input,
                    "Password input": self._password_input,
                    "OTP checkbox": self._use_otp_checkbox,
                    "Login button": self._login_btn,
                    "Back to Igoristan link": self._back_to_igoristan_link,
                },
                page_title=_PAGE_TITLE,
                timeout=timeout,
            )

            WebDriverWait(self._driver, timeout).until(ec.title_contains("Dashboard"))

            WebDriverWait(self._driver, timeout).until(
                ec.text_to_be_present_in_element(
                    (By.TAG_NAME, "h1"),
                    "Authentication Required",
                )
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def click_back_to_igoristan_link(self) -> DashboardLoginPage:
        """Click on the back to Igoristan link."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._back_to_igoristan_link)
        ).click()

        WebDriverWait(self._driver, timeout).until(
            ec.invisibility_of_element_located(self._back_to_igoristan_link)
        )

        return self

    def login_without_otp(self, creds: ImmutableCredentials) -> DashboardLoginPage:
        """Fill creds and trigger login btn."""
        timeout = get_timeout()

        username_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._username_input)
        )
        username_input.clear()
        username_input.send_keys(creds["login"])

        password_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._password_input)
        )
        password_input.clear()
        password_input.send_keys(creds["password"])

        self._login_without_otp_action_dispatchers[
            self._get_random_login_without_otp_action_key()
        ]()

        return self

    def login_without_otp_and_with_retries(
        self,
        creds: ImmutableCredentials,
        retries: int,
        *,
        logger: ILogger,
    ) -> DashboardLoginPage:
        """Fill creds and click on the login btn (n retries)."""
        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1

        while attempts_count <= retries:
            self.login_without_otp(creds)

            timeout = get_timeout()
            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.invisibility_of_element_located(self._password_input)
                )
                break

            msg = (
                "Failed to connect to the dashboard, without OTP."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = (
            "Connected to the dashboard, without OTP."
            " "
            f"After {attempts_count} attempt{s}."
        )

        logger.info(msg)

        return self

    def start_to_login_with_otp(
        self,
        creds: ImmutableCredentials,
        *,
        username_cache_key: str,
        otp_send_button_click_date_cache_key: str,
        cache: CacheRegion,
    ) -> DashboardLoginPage:
        """Enable OTP, fill fields and confirm to reach the OTP screen."""

        def _send(username: str) -> None:
            cache.set(username_cache_key, username)
            cache.set(
                otp_send_button_click_date_cache_key,
                datetime.now(UTC).isoformat(),
            )

            self._login_with_otp_action_dispatchers[
                self._get_random_login_with_otp_action_key()
            ]()

        username = creds["login"]
        timeout = get_timeout()
        igor_api_key = create_env_getters().get_value("igor_api_key")

        checkbox = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._use_otp_checkbox)
        )
        checkbox_label = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._use_otp_checkbox_label)
        )

        if not checkbox.is_selected():
            checkbox_label.click()

        validate(checkbox.is_selected(), name="checkbox_is_selected").assert_that(
            is_truthy, msg="Couldn't select the OTP checkbox."
        ).execute().raise_if_invalid()

        username_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._username_input)
        )
        username_input.clear()
        username_input.send_keys(username)

        password_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._password_input)
        )
        password_input.clear()
        password_input.send_keys(creds["password"])

        igor_api_key_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._igor_api_key_input)
        )
        igor_api_key_input.clear()
        igor_api_key_input.send_keys(igor_api_key)

        workers = get_max_workers()

        if workers > 1:
            with _get_lock():
                time.sleep(math.ceil(max(workers / 2, 2.5)))
                _send(username)
        else:
            _send(username)

        return self

    def start_to_login_with_otp_and_with_retries(  # noqa: PLR0913
        self,
        creds: ImmutableCredentials,
        retries: int,
        *,
        username_cache_key: str,
        otp_send_button_click_date_cache_key: str,
        logger: ILogger,
        cache: CacheRegion,
    ) -> DashboardLoginPage:
        """Enable OTP, fill fields and confirm to reach the OTP screen (n retries)."""
        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1

        while attempts_count <= retries:
            self.start_to_login_with_otp(
                creds,
                username_cache_key=username_cache_key,
                otp_send_button_click_date_cache_key=otp_send_button_click_date_cache_key,
                cache=cache,
            )

            timeout = get_timeout()

            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.invisibility_of_element_located(self._password_input)
                )
                break

            msg = (
                "Failed to reach the OTP screen."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = f"Reached the OTP screen.\nAfter {attempts_count} attempt{s}."

        logger.info(msg)

        return self

    def verify_invalid_creds_msg_is_displayed(self) -> DashboardLoginPage:
        """Verify the invalid creds msg is displayed."""
        try:
            timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "Invalid credentials msg": self._invalid_credentials_msg,
                },
                timeout=timeout,
            )

        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def verify_otp_screen(self) -> DashboardLoginPage:
        """Verify the OTP screen."""
        try:
            timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "OTP field": self._otp_field_on_otp_screen,
                },
                page_title="the Igoristan dashboard login page (OTP screen)",
                timeout=timeout,
            )
        except Exception as exc:
            raise PageVerificationError from exc
        else:
            return self

    def type_otp(
        self,
        *,
        username_cache_key: str,
        otp_send_button_click_date_cache_key: str,
        logger: ILogger,
        cache: CacheRegion,
    ) -> DashboardLoginPage:
        """Type the OTP code and confirm it."""
        unsafe_username: Any = cache.get(username_cache_key)
        unsafe_min_date: Any = cache.get(otp_send_button_click_date_cache_key)

        try:
            chain_validations(
                validate(unsafe_username, name="cached_to_address")
                .assert_that(is_not_none)
                .assert_that(is_str),
                validate(unsafe_min_date, name="cached_min_date")
                .assert_that(is_not_none)
                .assert_that(is_str)
                .assert_that(is_iso_date_string)
                .assert_that(is_iso_utc_date_string),
            ).execute().raise_if_invalid()
        except Exception as exc:
            raise TransientError from exc

        username: str = unsafe_username
        min_utc_date = datetime.fromisoformat(unsafe_min_date)

        msg = f"min_utc_date: {min_utc_date}"
        logger.info(msg)

        timeout = get_timeout()

        otp_code = retrieve_dashboard_otp_code(
            min_utc_date=min_utc_date, timeout=timeout
        )

        if otp_code is None:
            msg = "No matching OTP found."
            raise TransientError(msg)

        msg = f"Found OTP: {otp_code}"
        logger.info(msg)

        msg = f"Username: {username}"
        logger.info(msg)

        otp_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._otp_field_on_otp_screen)
        )
        otp_input.clear()
        otp_input.send_keys(otp_code)

        self._confirm_otp_action_dispatchers[
            self._get_random_confirm_otp_action_key()
        ]()

        return self

    def type_otp_with_retries(
        self,
        retries: int,
        *,
        username_cache_key: str,
        otp_send_button_click_date_cache_key: str,
        logger: ILogger,
        cache: CacheRegion,
    ) -> DashboardLoginPage:
        """Enable OTP, fill fields and confirm to reach the OTP screen (n retries)."""
        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1

        while attempts_count <= retries:
            self.type_otp(
                logger=logger,
                username_cache_key=username_cache_key,
                otp_send_button_click_date_cache_key=otp_send_button_click_date_cache_key,
                cache=cache,
            )

            timeout = get_timeout()

            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.invisibility_of_element_located(self._otp_field_on_otp_screen)
                )
                break

            msg = (
                "Failed to escape the OTP screen."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = f"Escaped the OTP screen.\nAfter {attempts_count} attempt{s}."

        logger.info(msg)

        return self
