"""Sending the chaotic form."""

from random import randint
from typing import TYPE_CHECKING

from ocarina.custom_types.scenario import Scenario
from ocarina.dsl.testing.selenium.create_test import create_selenium_test
from ocarina.dsl.testing.selenium.create_watcher import create_selenium_watcher
from ocarina.opinionated.dsl.drive_page import drive_page

from lib.connectors.test_steps.actions.chaotic_form import (
    fill_chaotic_form_and_send_it_with_retries,
    open_chaotic_form_page,
    verify_chaotic_form_page,
)
from lib.ext.ocarina.adapters.agnostic.act import act
from lib.ext.ocarina.adapters.selenium.logs import (
    create_just_log_error,
    create_log_success_with_current_url_and_take_screenshot,
)
from lib.ext.selenium.humanize.proxy import HumanizedDriver
from lib.ext.selenium.watchers.catch_me_if_you_can_watcher import (
    catch_me_if_you_can_cb,
)
from pages.chaotic_form import ChaoticFormPage

if TYPE_CHECKING:
    from ocarina.ports.ilogger import ILogger
    from selenium.webdriver.remote.webdriver import WebDriver


def _send_chaotic_form(driver: WebDriver, logger: ILogger):  # noqa: ANN202
    """Send the chaotic form (full path)."""
    on_chaotic_form_page = ChaoticFormPage(driver=driver)

    just_log_error = create_just_log_error(logger=logger)
    log_success_with_current_url_and_take_screenshot = (
        create_log_success_with_current_url_and_take_screenshot(
            logger=logger, driver=driver
        )
    )

    return [
        drive_page(
            act(on_chaotic_form_page, open_chaotic_form_page)
            .failure(
                just_log_error(
                    "Failed to open the chaotic form page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Opened the chaotic form page!"
                )
            ),
            act(on_chaotic_form_page, verify_chaotic_form_page)
            .failure(
                just_log_error(
                    "Failed to verify the chaotic form page...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Verified the chaotic form page!"
                )
            ),
            act(
                on_chaotic_form_page,
                fill_chaotic_form_and_send_it_with_retries(
                    retries=10,
                    logger=logger,
                    cinto_height=1,
                    corsican_city="Hello world. I have no idea of what I do!",
                    personal_revelation=(
                        "This form is incredibly permissive,"
                        " "
                        "I don't even know what to write here."
                    ),
                    inspiring_apostle_index=randint(1, 5),  # noqa: S311
                    bible_verse=(
                        "A V E  M A R I A,"
                        "  "
                        "F U L L  O F  G R A C E,"
                        "  "
                        "T H E  L O R D  I S  W I T H  T H E E."
                    ),
                ),
            )
            .failure(
                just_log_error(
                    "Failed to send the chaotic form...",
                )
            )
            .success(
                log_success_with_current_url_and_take_screenshot(
                    "Sent the chaotic form!"
                )
            ),
        ),
    ]


test_send_chaotic_form = create_selenium_test(
    name="Send the chaotic form",
    test_scenario=lambda driver, logger: Scenario(
        test_chain=_send_chaotic_form(
            HumanizedDriver(
                driver,
                wpm=125,
                typo_rate=0.14,
                hesitation_rate=0.02,
                burst_rate=0.35,
                late_correction_rate=0.6,
            ),
            logger,
        ),
        watchers=[
            create_selenium_watcher(
                callback=catch_me_if_you_can_cb,
                name="catch-me-if-you-can",
                poll_interval=0.8,
            ),
        ],
    ),
)
