"""OTP history getter function."""

from typing import Any

import requests

from api.constants.endpoints import OTP_HISTORY_ENDPOINT_URL


def get_otp_history(*, igor_api_key: str, timeout: int) -> Any:  # noqa: ANN401
    """Get OTP history."""
    response = requests.get(
        OTP_HISTORY_ENDPOINT_URL,
        headers={"x-api-key": igor_api_key},
        timeout=timeout,
    )
    return response.json()
