"""Igoristan's corsicamon main page."""

import random
from contextlib import suppress
from typing import TYPE_CHECKING, Literal, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.dsl.invariants.assertions import is_positive
from ocarina.dsl.invariants.validate import validate
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.corsicamon import CORSICAMON_PAGE_URL
from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout
from lib.ext.ocarina.adapters.selenium.screenshotter import take_screenshot
from lib.ext.selenium.pages.verify_elements_presence import verify_elements_presence

if TYPE_CHECKING:
    from ocarina.custom_types.effect import Effect
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.common.by import ByType
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class CorsicamonPage(SeleniumTitleMixin, POMBase):
    """Igoristan's corsicamon main page."""

    def __init__(self, *, driver: WebDriver, url: str = CORSICAMON_PAGE_URL) -> None:
        """Initialize dashboard login POM."""
        self._URL = url
        self._driver = driver

        self._back_to_igoristan_link = (By.CSS_SELECTOR, 'a[href="/igoristan/"]')
        self._new_draw_btn = (
            By.CSS_SELECTOR,
            '[data-testid="new-draw-btn"]',
        )

        self._corsicamon_network_error_container = (
            By.CSS_SELECTOR,
            '[data-testid="corsicadex-network-error"]',
        )
        self._corsicamon_network_error_retry_btn = (
            By.CSS_SELECTOR,
            '[data-testid="corsicadex-network-error-retry-btn"]',
        )

        self._enter_id_input = (By.ID, "enter-id-input")
        self._add_corsicamon_btn = (
            By.CSS_SELECTOR,
            '[data-testid="add-corsicamon-btn"]',
        )

        self._invalid_id_msg = (
            By.XPATH,
            "//*[contains(text(), 'Please enter a valid Corsicamon ID')]",
        )

        self._already_in_draw_msg = (
            By.XPATH,
            "//*[contains(text(), 'is already in your draw!')]",
        )

        self._draw_complete_msg = (
            By.XPATH,
            "//*[contains(text(), 'Draw Complete!')]",
        )

        self._failed_to_add_corsicamon_msg = (
            By.XPATH,
            "//*[contains(text(), 'Failed to load Corsicamon. Please try again.')]",
        )

        timeout = get_timeout()

        self._add_corsicamon_dispatchers: dict[str, Effect] = {
            "focus_add_corsicamon_input_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._add_corsicamon_btn))
                .send_keys(Keys.ENTER)
            ),
            "click_add_corsicamon_button": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._add_corsicamon_btn))
                .click()
            ),
            "focus_add_corsicamon_button_then_press_enter": lambda: (
                WebDriverWait(self._driver, timeout)
                .until(ec.visibility_of_element_located(self._add_corsicamon_btn))
                .send_keys(Keys.ENTER)
            ),
        }

    def _get_random_add_corsicamon_dispatchers_key(self) -> str:
        return random.choice(  # noqa: S311
            list(self._add_corsicamon_dispatchers.keys())
        )

    @staticmethod
    def _corsicamon_card_id(idx: int) -> tuple[ByType, str]:
        """Corsicamon card ID area selector."""
        return (
            By.CSS_SELECTOR,
            f'[data-testid="pokemon-id-{idx}"]',
        )

    def open(self) -> CorsicamonPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> CorsicamonPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            verify_elements_presence(
                driver=self._driver,
                selectors={
                    "New draw button": self._new_draw_btn,
                    "Back to Igoristan link": self._back_to_igoristan_link,
                    "Add Corsicamon button": self._add_corsicamon_btn,
                    "Enter Corsicamon ID button": self._enter_id_input,
                    "First Corsicamon card": self._corsicamon_card_id(1),
                    "Second Corsicamon card": self._corsicamon_card_id(2),
                    "Third Corsicamon card": self._corsicamon_card_id(3),
                },
                page_title="Corsicamon page",
                timeout=timeout,
            )

            needle = "Corsicamon"

            WebDriverWait(self._driver, timeout).until(ec.title_contains(needle))
        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def click_back_to_igoristan_link(self) -> CorsicamonPage:
        """Click on the back to Igoristan link."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._back_to_igoristan_link)
        ).click()

        WebDriverWait(self._driver, timeout).until(
            ec.invisibility_of_element_located(self._back_to_igoristan_link)
        )

        return self

    def enter_invalid_corsicamon_id(self) -> CorsicamonPage:
        """Enter the -1 id, then check the presence of an error message."""
        timeout = get_timeout()

        enter_id_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._enter_id_input)
        )
        enter_id_input.clear()
        enter_id_input.send_keys("-1")

        self._add_corsicamon_dispatchers[
            self._get_random_add_corsicamon_dispatchers_key()
        ]()

        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._invalid_id_msg)
        )

        return self

    def enter_already_in_draw_corsicamon_id(self) -> CorsicamonPage:
        """Enter already in draw id, then check the presence of an error message."""
        timeout = get_timeout()

        corsicamon_id = (
            WebDriverWait(self._driver, timeout)
            .until(
                ec.visibility_of_element_located(
                    self._corsicamon_card_id(random.randint(1, 3))  # noqa: S311
                )
            )
            .text.replace("#", "")
        )

        enter_id_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._enter_id_input)
        )
        enter_id_input.clear()
        enter_id_input.send_keys(corsicamon_id)

        self._add_corsicamon_dispatchers[
            self._get_random_add_corsicamon_dispatchers_key()
        ]()

        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._already_in_draw_msg)
        )

        return self

    def enter_fresh_corsicamon_id(self, *, skip_check: bool = False) -> CorsicamonPage:
        """Enter fresh id, then check the presence of an error message."""
        timeout = get_timeout()

        def _get_corsicamon_ids(driver: WebDriver) -> list[str] | Literal[False]:
            try:
                return [
                    driver.find_element(*self._corsicamon_card_id(i)).text.replace(
                        "#", ""
                    )
                    for i in range(1, 4)
                ]
            except Exception:  # noqa: BLE001
                return False

        corsicamon_ids: list[str] = WebDriverWait(self._driver, timeout).until(
            _get_corsicamon_ids
        )

        corsicamon_id = random.choice(  # noqa: S311
            [str(i) for i in range(1, 9) if str(i) not in corsicamon_ids]
        )

        enter_id_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._enter_id_input)
        )
        enter_id_input.clear()
        enter_id_input.send_keys(corsicamon_id)

        self._add_corsicamon_dispatchers[
            self._get_random_add_corsicamon_dispatchers_key()
        ]()

        if not skip_check:
            timeout = 20  # Hard-coded since loaders are slow here.
            WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(self._draw_complete_msg)
            )

        return self

    def enter_fresh_corsicamon_id_with_retries(
        self, *, retries: int, logger: ILogger
    ) -> CorsicamonPage:
        """Enter fresh Corsicamon ID (n retries)."""
        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1
        while attempts_count <= retries:
            self.enter_fresh_corsicamon_id(skip_check=True)
            timeout = get_timeout()
            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.invisibility_of_element_located(self._new_draw_btn)
                )
                break

            msg = (
                "Failed to enter fresh Corsicamon ID."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = f"Entered the fresh Corsicamon ID. After {attempts_count} attempt{s}."

        logger.info(msg)
        return self

    def make_a_new_draw(self, *, skip_check: bool = False) -> CorsicamonPage:
        """Make a new draw."""
        timeout = get_timeout()

        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._new_draw_btn)
        ).click()

        if not skip_check:
            timeout = 20  # Hard-coded since loaders are slow here.
            WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(self._new_draw_btn)
            )

        return self

    def make_a_new_draw_with_retries(
        self, *, retries: int, logger: ILogger
    ) -> CorsicamonPage:
        """Make a new draw (n retries)."""

        def _click_retry_button() -> CorsicamonPage:
            timeout = get_timeout()
            WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(
                    self._corsicamon_network_error_retry_btn
                )
            ).click()

            return self

        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1
        self.make_a_new_draw(skip_check=True)
        while attempts_count <= retries:
            timeout = 20  # Hard-coded since loaders are slow here.
            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.visibility_of_element_located(self._new_draw_btn)
                )
                break

            msg = (
                "Failed to make a new draw."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            _click_retry_button()
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = f"Made a new draw. After {attempts_count} attempt{s}."

        logger.info(msg)
        return self

    def verify_enter_id_field_empty(self) -> CorsicamonPage:
        """Verify enter ID field is empty."""
        timeout = get_timeout()

        def _input_is_empty(driver: WebDriver) -> bool:
            el = driver.find_element(*self._enter_id_input)
            return el.get_attribute("value") == ""

        WebDriverWait(self._driver, timeout).until(_input_is_empty)

        return self
