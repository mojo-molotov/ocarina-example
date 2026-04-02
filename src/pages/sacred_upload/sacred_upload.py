"""Igoristan's random error page."""

import random
from pathlib import Path
from typing import TYPE_CHECKING, final

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.dsl.invariants.assertions import is_not_zero, is_positive
from ocarina.dsl.invariants.validate import validate

# ruff: noqa: S101
from ocarina.infra.selenium.mixins import SeleniumTitleMixin
from ocarina.pom.base import POMBase
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from constants.pages.sacred_upload import SACRED_UPLOAD_PAGE_URL
from lib.ext.ocarina.adapters.agnostic.cli_getters import get_timeout

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class SacredUploadPage(SeleniumTitleMixin, POMBase):
    """Igoristan's sacred upload page."""

    def __init__(self, *, driver: WebDriver, url: str = SACRED_UPLOAD_PAGE_URL) -> None:
        """Initialize sacred upload POM."""
        self._driver = driver
        self._URL = url

        self._images_input = (
            By.ID,
            "images",
        )

        self._previews_container_selector = (
            '[data-testid="upload-form-previews-container"]'
        )
        self._previews_container = (
            By.CSS_SELECTOR,
            self._previews_container_selector,
        )
        self._upload_btn = (
            By.CSS_SELECTOR,
            '[data-testid="upload-btn"]',
        )
        self._amen_btn = (
            By.CSS_SELECTOR,
            '[data-testid="amen-btn"]',
        )

    def open(self) -> SacredUploadPage:
        """Open the page."""
        self._driver.get(self._URL)
        return self

    def verify(self, *, timeout: float | None = None) -> SacredUploadPage:
        """Verify function."""
        try:
            if timeout is None:
                timeout = get_timeout()

            expected_title_needle = "Blessed file upload simulator"
            expected_h1 = "Upload images!"

            WebDriverWait(self._driver, timeout).until(
                ec.title_contains(expected_title_needle)
            )

            h1 = WebDriverWait(self._driver, timeout).until(
                ec.presence_of_element_located((By.TAG_NAME, "h1"))
            )

            assert h1.text.lower() == expected_h1.lower(), (
                f"Unexpected h1 text: '{h1.text}'"
            )
        except Exception as exc:
            raise PageVerificationError from exc

        return self

    def add_images(self, *, images_amount: int) -> SacredUploadPage:
        """Add images to the sacred upload form."""
        validate(images_amount, name="images_amount").assert_that(
            is_positive
        ).assert_that(is_not_zero).execute().raise_if_invalid()

        timeout = get_timeout()

        root = Path(__file__).parent / "fixtures"
        img_paths = [
            root / "bayu_bayushki_bayu.jpg",
            root / "cozy_bear.jpg",
            root / "napoleon.jpg",
        ]

        file_input = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._images_input)
        )

        selected = "\n".join(
            str(random.choice(img_paths))  # noqa: S311
            for _ in range(images_amount)
        )

        file_input.send_keys(selected)

        previews_img_selector = f"{self._previews_container_selector} img"

        WebDriverWait(self._driver, timeout).until(
            lambda driver: (
                len(driver.find_elements(By.CSS_SELECTOR, previews_img_selector))
                == images_amount
            )
        )

        return self

    def click_on_upload_btn(self) -> SacredUploadPage:
        """Click on upload button."""
        timeout = get_timeout()
        upload_btn = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._upload_btn)
        )
        upload_btn.click()
        return self

    def click_on_amen_btn(self) -> SacredUploadPage:
        """Click on amen button."""
        timeout = get_timeout()
        amen_btn = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._amen_btn)
        )
        amen_btn.click()
        return self

    def verify_dropzone_is_empty(self) -> SacredUploadPage:
        """Verify dropzone is empty."""
        previews_img_selector = f"{self._previews_container_selector} img"

        timeout = 20  # Hard-coded since loaders are slow here.

        WebDriverWait(self._driver, timeout).until(
            lambda driver: (
                len(driver.find_elements(By.CSS_SELECTOR, previews_img_selector)) == 0
            )
        )
        return self
