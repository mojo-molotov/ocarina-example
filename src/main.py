"""Napoleon approves."""

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from ocarina.dsl.testing.oc_test_cycle import has_test_cycle_failed
from ocarina.infra.selenium.create_drivers_pool import create_selenium_drivers_pool
from ocarina.opinionated.cli.selenium.cli_store_singleton import (
    SeleniumCliStoreSingleton,
)
from ocarina.opinionated.cli.selenium.cli_store_singleton import (
    SeleniumCliStoreSingleton as CliStoreSingleton,
)
from ocarina.opinionated.cli.selenium.create_cli_store import (
    create_selenium_auto_cli_store,
)
from ocarina.opinionated.launcher.bootstrap import bootstrap, run_plugins
from ocarina.opinionated.loggers.create_matching_logger import (
    create_matching_logger,
    get_default_log_dir,
)
from ocarina.opinionated.loggers.print_logger import PrintLogger
from ocarina.opinionated.loggers.utils.format_metadata_str import (
    concat_metadata,
    format_current_thread_metadata_str,
    format_utc_date_metadata_str,
)
from ocarina.opinionated.plugins.reports.docx_tests_proofs import generate_docx_proof
from ocarina.opinionated.plugins.reports.pretty_print_results import (
    pretty_print_results,
)
from ocarina.opinionated.plugins.reports.results_to_json import generate_json_results
from ocarina.opinionated.plugins.reports.timing import timing

from lib.ext.redis.client import warmup_redis_client
from tests.cycles.e2e import create_e2e_test_cycle

if TYPE_CHECKING:
    from ocarina.custom_types.oc_test_layers import TestCycleResults

if __name__ == "__main__":
    CliStoreSingleton().push(create_selenium_auto_cli_store())

    drivers_pool = create_selenium_drivers_pool(
        browser=SeleniumCliStoreSingleton().get("browser"),
        driver_path=SeleniumCliStoreSingleton().get("driver_path"),
        headless=SeleniumCliStoreSingleton().get("headless"),
        wait_timeout=SeleniumCliStoreSingleton().get("wait_timeout"),
        max_size=SeleniumCliStoreSingleton().get("workers"),
    )

    logger = create_matching_logger(CliStoreSingleton().get("logger"))

    logger.info("Warming up the Redis client...")
    warmup_redis_client()
    logger.success("Redis client initialized!")

    def _post_exec(results: TestCycleResults) -> None:
        print()  # noqa: T201
        pretty_print_results(results, with_colors=True)
        if has_test_cycle_failed(results):
            sys.exit(1)

    with timing(prefix="Tests duration:"):
        bootstrap(
            post_exec=_post_exec,
            test_cycle=create_e2e_test_cycle(drivers_pool),
            run_plugins=lambda results: run_plugins(
                lambda: generate_docx_proof(
                    logs_root=get_default_log_dir(),
                    logger=create_matching_logger("terminal").set_domain_taxonomy(
                        ("Generate DOCX proofs plugin",)
                    ),
                    output_root=Path.cwd() / ".reports" / "tests_docx_output",
                ),
                lambda: generate_json_results(
                    results=results,
                    output_dir=Path.cwd() / ".reports" / "tests_json_output",
                    logger=create_matching_logger("terminal").set_domain_taxonomy(
                        ("Generate JSON report file plugin",)
                    ),
                ),
                exceptions_logger=PrintLogger()
                .set_prefix(
                    lambda: concat_metadata(
                        format_utc_date_metadata_str, format_current_thread_metadata_str
                    )
                )
                .set_domain_taxonomy(("Post-execution plugins",)),
            ),
        )
