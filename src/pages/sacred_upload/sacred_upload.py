"""Igoristan's sacred upload page."""

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
    from collections.abc import Callable

    from selenium.webdriver.common.by import ByType
    from selenium.webdriver.remote.webdriver import WebDriver


def _wait_for_previews(expected_len: int, selector: str) -> Callable[[WebDriver], bool]:
    def unwrapped(driver: WebDriver) -> bool:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        current_len = len(elements)
        return current_len == expected_len

    return unwrapped


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
        self._sin_btn = (
            By.CSS_SELECTOR,
            '[data-testid="forgive-me-btn"]',
        )

        self._images_dropzone_error_message = (
            By.CSS_SELECTOR,
            '[data-testid="images-dropzone-error-msg"]',
        )
        self._igoristan_link = (By.CSS_SELECTOR, 'a[href="/igoristan/"]')

    @staticmethod
    def _delete_img_btn(idx: int) -> tuple[ByType, str]:
        """Delete image btn selector."""
        return (
            By.CSS_SELECTOR,
            f'[data-testid="delete-image-{idx}-btn"]',
        )

    def _verify_images_dropzone_error_message(
        self, error_message_needle: str
    ) -> SacredUploadPage:
        """Verify dropzone error message contains the needle."""
        timeout = get_timeout()
        images_dropzone_error_message = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._images_dropzone_error_message)
        )
        t = images_dropzone_error_message.text
        assert error_message_needle in t, (
            f"error_message_needle not found, got: {t}."
            " "
            f"Expected needle: {error_message_needle}"
        )

        return self

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

    def add_images(
        self,
        *,
        images_amount: int,
        failing: bool = False,
        forced_expected_img_amount: int = -1,
    ) -> SacredUploadPage:
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

        self._driver.execute_script("arguments[0].value = '';", file_input)

        selected = "\n".join(
            str(random.choice(img_paths))  # noqa: S311
            for _ in range(images_amount)
        )

        file_input.send_keys(selected)

        previews_img_selector = f"{self._previews_container_selector} img"

        if failing:
            self._verify_images_dropzone_error_message(error_message_needle="Maximum")
        else:
            expected_len = (
                forced_expected_img_amount
                if forced_expected_img_amount >= 0
                else images_amount
            )
            WebDriverWait(self._driver, timeout).until(
                _wait_for_previews(expected_len, previews_img_selector),
                message=(
                    f"Expected {expected_len}"
                    " "
                    f"preview images (selector: '{previews_img_selector}')"
                ),
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

    def click_on_delete_img_btn(self, idx: int) -> SacredUploadPage:
        """Click on upload button."""
        timeout = get_timeout()
        delete_img_btn = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._delete_img_btn(idx))
        )
        delete_img_btn.click()
        return self

    def click_on_amen_btn(self) -> SacredUploadPage:
        """Click on amen button."""
        timeout = get_timeout()
        amen_btn = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._amen_btn)
        )
        amen_btn.click()
        return self

    def click_on_sin_btn(self) -> SacredUploadPage:
        """Click on sin button."""
        timeout = get_timeout()
        sin_btn = WebDriverWait(self._driver, timeout).until(
            ec.presence_of_element_located(self._sin_btn)
        )
        sin_btn.click()
        return self

    def verify_dropzone_is_empty(self) -> SacredUploadPage:
        """Verify dropzone is empty."""
        previews_img_selector = f"{self._previews_container_selector} img"

        timeout = 20  # Hard-coded since loaders are slow here.
        expected_len = 0

        WebDriverWait(self._driver, timeout).until(
            _wait_for_previews(expected_len, previews_img_selector),
            message=f"Expected {expected_len} preview image.",
        )
        return self

    def click_back_to_igoristan_link(self) -> SacredUploadPage:
        """Click on the back to Igoristan link."""
        timeout = get_timeout()
        WebDriverWait(self._driver, timeout).until(
            ec.visibility_of_element_located(self._igoristan_link)
        ).click()

        WebDriverWait(self._driver, timeout).until(
            ec.invisibility_of_element_located(self._igoristan_link)
        )

        return self
