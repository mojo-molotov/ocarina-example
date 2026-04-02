"""Utilities to verify elements presence on a page."""

from typing import TYPE_CHECKING

from ocarina.custom_errors.test_framework.pages import PageVerificationError
from ocarina.dsl.invariants.assertions import is_positive
from ocarina.dsl.invariants.validate import validate
from ocarina.infra.selenium.driver_healthcheck import driver_healthcheck
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


def verify_elements_presence(
    *,
    driver: WebDriver,
    selectors: dict[str, tuple[str, str]],
    timeout: float | None,
    page_title: str = "",
) -> None:
    """Check that all given selectors are visible on the page."""
    validate(len(selectors), name="selectors_amount").assert_that(
        is_positive
    ).execute().raise_if_invalid()

    errors: list[str] = []

    normalized_timeout = timeout if timeout is not None else 10.0

    for element_name, (by, value) in selectors.items():
        driver_healthcheck(driver)
        try:
            WebDriverWait(driver, normalized_timeout).until(
                ec.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            if page_title:
                errors.append(
                    f"{element_name} not found with '{value}'"
                    " "
                    f"({by}): not on {page_title}."
                )
            else:
                errors.append(f"{element_name} not found with '{value}' ({by}).")

    if errors:
        raise PageVerificationError("\n".join(errors))
