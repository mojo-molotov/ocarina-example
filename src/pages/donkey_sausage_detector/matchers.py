"""DSED -> Matchers."""

from typing import TYPE_CHECKING, final

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


@final
class DSEDPageMatchers:
    """No Sicilian allowed."""

    def __init__(self, *, driver: WebDriver) -> None:
        """Initialize helper."""
        self._driver = driver

    def is_bsod_page(self) -> bool:
        """Quickly verify is BSOD page."""
        timeout = 30  # Hard-coded since loaders are slow here.

        try:
            WebDriverWait(self._driver, timeout).until(
                ec.title_contains("You donkey sausage eater!")
            )
        except TimeoutException:
            return False
        return True

    def is_ids_bypassed_page(self) -> bool:
        """Quickly verify is 'success' page."""
        timeout = 30  # Hard-coded since loaders are slow here.

        try:
            WebDriverWait(self._driver, timeout).until(
                ec.title_contains("The donkey sausage eater detector")
            )
        except TimeoutException:
            return False
        return True
