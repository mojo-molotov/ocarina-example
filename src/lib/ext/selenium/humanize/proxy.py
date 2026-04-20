"""Transparent Selenium wrappers that make every send_keys call human-like.

HumanizedDriver and HumanizedWebElement act as drop-in replacements for
Selenium's WebDriver and WebElement. Any call to send_keys is automatically
routed through humanized_send_keys — no changes required in the rest of
the codebase.

Usage:
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    from lib.ext.selenium.humanize.driver import HumanizedDriver

    raw_driver = webdriver.Chrome()
    driver = HumanizedDriver(raw_driver, wpm=75, typo_rate=0.06)

    driver.get("https://example.com/login")
    driver.find_element(By.ID, "username").send_keys("human.on.tinder@mail.com")
    driver.find_element(By.ID, "password").send_keys("hunter2")

Both classes use __getattr__ to delegate every attribute or method that is
not explicitly overridden to the underlying Selenium object, so the full
Selenium API remains available without any extra boilerplate.
"""

from typing import TYPE_CHECKING, Any, Unpack

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from lib.ext.selenium.humanize.keyboard import (
    KeyboardConfig,
    humanized_send_keys_with_config,
)

if TYPE_CHECKING:
    from selenium.webdriver.support.relative_locator import RelativeBy


class _HumanizedWebElement(WebElement):
    """Proxy for a Selenium WebElement with a humanized send_keys.

    Every method and attribute not explicitly defined here is transparently
    delegated to the underlying WebElement via __getattr__, so this class
    can be used as a drop-in replacement anywhere a WebElement is expected.
    """

    def __init__(self, element: WebElement, keyboard_config: KeyboardConfig) -> None:
        """Wrap a WebElement with the given humanized-typing configuration.

        Args:
            element:         The real Selenium WebElement to wrap.
            keyboard_config: Keyword arguments forwarded verbatim to
                             humanized_send_keys (e.g. wpm, typo_rate).

        """
        object.__init__(self)
        self._element = element
        self._config = keyboard_config

    def send_keys(self, *value: Any) -> None:  # noqa: ANN401
        """Type into the element using humanized_send_keys.

        All positional arguments are joined into a single string, matching
        the signature of the native Selenium send_keys.

        Args:
            *value: One or more values to type. Non-string values are cast
                    to str before joining.

        """
        for v in value:
            if isinstance(v, str):
                humanized_send_keys_with_config(self._element, v, self._config)
            else:
                self._element.send_keys(v)

    def __getattr__(self, name: str):  # noqa: ANN204
        """Delegate any unrecognized attribute to the underlying WebElement.

        Args:
            name: Attribute or method name requested by the caller.

        Returns:
            The corresponding attribute from the wrapped WebElement.

        """
        return getattr(self._element, name)


class HumanizedDriver(WebDriver):
    """Proxy for a Selenium WebDriver that returns HumanizedWebElements.

    Wraps find_element and find_elements so that every element returned by
    this driver automatically uses humanized_send_keys. All other driver
    methods (get, quit, implicitly_wait, etc.) are transparently forwarded
    to the underlying WebDriver via __getattr__.
    """

    def __init__(
        self, driver: WebDriver, **keyboard_config: Unpack[KeyboardConfig]
    ) -> None:
        """Wrap a WebDriver with a shared humanized-typing configuration.

        Args:
            driver:           The real Selenium WebDriver to wrap.
            **keyboard_config: Keyword arguments forwarded verbatim to
                              humanized_send_keys on every element returned
                              by this driver (e.g. wpm=75, typo_rate=0.06).

        """
        object.__init__(self)
        self._driver = driver
        self._config = keyboard_config

    def find_element(
        self,
        by: str | RelativeBy = "id",
        value: str | None = None,
    ) -> _HumanizedWebElement:
        """Find a single element and return it wrapped in HumanizedWebElement.

        Args:
            by:    Selenium locator strategy (e.g. By.ID, By.CSS_SELECTOR).
            value: Locator value matching the chosen strategy.

        Returns:
            A HumanizedWebElement wrapping the matched element.

        """
        element = self._driver.find_element(by, value)
        return _HumanizedWebElement(element, self._config)

    def find_elements(
        self,
        by: str | RelativeBy = "id",
        value: str | None = None,
    ) -> list[WebElement]:
        """Find all matching elements and return them wrapped in HumanizedWebElement.

        Args:
            by:    Selenium locator strategy (e.g. By.ID, By.CSS_SELECTOR).
            value: Locator value matching the chosen strategy.

        Returns:
            A list of HumanizedWebElements wrapping the matched elements.
            Returns an empty list if no elements are found.

        """
        elements = self._driver.find_elements(by, value)
        return [_HumanizedWebElement(el, self._config) for el in elements]

    def __getattr__(self, name: str):  # noqa: ANN204
        """Delegate any unrecognized attribute to the underlying WebDriver.

        Args:
            name: Attribute or method name requested by the caller.

        Returns:
            The corresponding attribute from the wrapped WebDriver.

        """
        return getattr(self._driver, name)
