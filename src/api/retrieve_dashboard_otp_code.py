"""OTP code retrieve function."""

from datetime import datetime, timedelta
from typing import Any

import requests

from api.consts.endpoints import OTP_HISTORY_ENDPOINT_URL
from lib.ext.ocarina.adapters.agnostic.env_getters import create_env_getters


def retrieve_dashboard_otp_code(*, min_utc_date: datetime, timeout: int) -> str | None:
    """Retrieve dashboard OTP code."""
    igor_api_key = create_env_getters().get_value("igor_api_key")
    response = requests.get(
        OTP_HISTORY_ENDPOINT_URL,
        headers={"x-api-key": igor_api_key},
        timeout=timeout,
    )
    entries = response.json()

    def _entry_matches(entry: dict[str, Any]) -> bool:
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
