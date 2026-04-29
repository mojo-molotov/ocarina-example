"""Igoristan's chaotic form page."""

from contextlib import suppress
from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.dsl.invariants.assertions import is_positive
from ocarina.dsl.invariants.validate import validate
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.chaotic_form import CHAOTIC_FORM_PAGE_URL
from lib.ext.ocarina.adapters.selenium.cli_getters import get_timeout
from lib.ext.ocarina.adapters.selenium.screenshotter import take_screenshot

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class ChaoticFormPage(SeleniumTitleMixin, POMBase):
    """Igoristan's chaotic form page."""

    def __init__(self, *, driver: WebDriver, url: str = CHAOTIC_FORM_PAGE_URL) -> None:
        """Initialize chaotic form POM."""
        self._driver = driver
        self._URL = url

        self._bible_verse_input = (By.ID, "bible-verse")
        self._corsican_city_input = (By.ID, "corsican-city")
        self._inspiring_apostle_input = (By.ID, "inspiring-apostle")
        self._cinto_height_input = (By.ID, "cinto-height")
        self._personal_revelation_input = (By.ID, "personal-revelation")
        self._submit_btn = (
            By.CSS_SELECTOR,
            '[data-testid="chaotic-form-submit-btn"]',
        )
        self._success_msg = (By.CSS_SELECTOR, '[data-testid="success-message"]')

    def open(self) -> ChaoticFormPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> ChaoticFormPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            WebDriverWait(self._driver, timeout).until(
                ec.title_contains("Chaotic form")
            )

            WebDriverWait(self._driver, timeout).until(
                ec.text_to_be_present_in_element(
                    (By.TAG_NAME, "h1"),
                    "Sacred Corsican Registration",
                )
            )
        except TimeoutException as exc:
            raise PageVerificationError from exc

        return self

    def _fill_form_and_send_it(  # noqa: PLR0913
        self,
        *,
        bible_verse: str,
        corsican_city: str,
        inspiring_apostle_index: int,
        cinto_height: float,
        personal_revelation: str,
        skip_final_check: bool = False,
    ) -> ChaoticFormPage:
        """Fill every field and submit the form.

        Args:
            bible_verse:             Text typed into the "Bible Verse" field.
            corsican_city:           Text typed into the "Corsican City" field.
            inspiring_apostle_index: Zero-based index of the option to select in the
                                     "Most Inspiring Apostle" dropdown. If the index
                                     exceeds the number of available options, the last
                                     option is selected instead. Must be >= 0.
            cinto_height:            Numeric value typed into the "Cinto Height" field.
            personal_revelation:     Text typed into the "Personal Revelation" field.
            skip_final_check:        Ignore the success message.

        Returns:
            The ChaoticFormPage instance, allowing method chaining.

        Raises:
            ValueError: If inspiring_apostle_index is negative.

        """
        validate(inspiring_apostle_index, name="inspiring_apostle_index").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        timeout = get_timeout()
        bible_verse_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._bible_verse_input)
        )
        bible_verse_input.click()
        bible_verse_input.clear()
        bible_verse_input.send_keys(bible_verse)

        corsican_city_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._corsican_city_input)
        )
        corsican_city_input.click()
        corsican_city_input.clear()
        corsican_city_input.send_keys(corsican_city)

        inspiring_apostle_element = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._inspiring_apostle_input)
        )
        select = Select(inspiring_apostle_element)
        options_count = len(select.options)
        clamped_index = min(inspiring_apostle_index, options_count - 1)
        select.select_by_index(clamped_index)

        cinto_height_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._cinto_height_input)
        )
        cinto_height_input.click()
        cinto_height_input.clear()
        cinto_height_input.send_keys(str(cinto_height))

        personal_revelation_input = WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._personal_revelation_input)
        )
        personal_revelation_input.click()
        personal_revelation_input.clear()
        personal_revelation_input.send_keys(personal_revelation)

        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._submit_btn)
        ).click()

        if not skip_final_check:
            WebDriverWait(self._driver, timeout).until(
                ec.visibility_of_element_located(self._success_msg)
            )

        return self

    def fill_form_and_send_it_with_retries(  # noqa: PLR0913
        self,
        *,
        retries: int,
        logger: ILogger,
        bible_verse: str,
        corsican_city: str,
        inspiring_apostle_index: int,
        cinto_height: float,
        personal_revelation: str,
    ) -> ChaoticFormPage:
        """Fill every field and submit the form (n retries)."""
        validate(retries, name="retries").assert_that(
            is_positive
        ).execute().raise_if_invalid()

        attempts_count = 1
        self._fill_form_and_send_it(
            bible_verse=bible_verse,
            corsican_city=corsican_city,
            inspiring_apostle_index=inspiring_apostle_index,
            cinto_height=cinto_height,
            personal_revelation=personal_revelation,
            skip_final_check=True,
        )
        while attempts_count <= retries:
            timeout = min(get_timeout(), 5)  # Hard-coded since toast is fast here.
            with suppress(Exception):
                WebDriverWait(self._driver, timeout).until(
                    ec.visibility_of_element_located(self._success_msg)
                )
                break

            msg = (
                "Failed to send the form."
                "\n"
                f"Life: {attempts_count}/{retries}"
                "\n"
                f"Current URL: {self._driver.current_url}"
            )

            logger.warning(msg)
            take_screenshot(driver=self._driver, logger=logger, category="WARNING")
            timeout = 20  # Hard-coded since loaders are slow here.
            WebDriverWait(self._driver, timeout).until(
                ec.element_to_be_clickable(self._submit_btn)
            ).click()
            attempts_count += 1

        s = "s" if attempts_count > 1 else ""
        msg = f"Sent the form. After {attempts_count} attempt{s}."

        logger.info(msg)
        return self
