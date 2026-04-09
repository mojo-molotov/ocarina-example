"""OTP code retrieve function."""

from datetime import datetime, timedelta
from typing import Any

from api.get_otp_history import get_otp_history
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters


def retrieve_dashboard_otp_code(
    *, min_utc_date: datetime, timeout: int, expected_login: str | None = None
) -> str | None:
    """Retrieve dashboard OTP code."""
    env = create_env_getters()
    igor_api_key = env.get_value("igor_api_key")
    entries = get_otp_history(igor_api_key=igor_api_key, timeout=timeout)

    def _entry_matches(entry: dict[str, Any]) -> bool:
        expected_user = expected_login or env.get_credentials("dashboard")["login"]
        is_testing_entry = entry["_user"] == expected_user
        if not is_testing_entry:
            return False

        created_at = datetime.fromisoformat(
            entry["createdAtTimestampLackingMsPrecision"]
        )
        return created_at >= min_utc_date - timedelta(seconds=1)

    matching = list(filter(_entry_matches, entries))

    if not matching:
        return None

    matching.sort(
        key=lambda e: e["createdAtTimestampLackingMsPrecision"],
    )
    otp: str = matching[0]["otpCode"]
    return otp
