
import secrets

from fastapi import Header, HTTPException, status

from app.config import get_api_key


def verify_api_key(
    x_api_key: str | None = Header(default=None),
) -> None:
    expected_key = get_api_key()

    if x_api_key is None or not secrets.compare_digest(
        x_api_key, expected_key
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
