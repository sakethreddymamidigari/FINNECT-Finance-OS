"""
Authentication utilities.

Contains helper functions to validate JWT tokens
and identify the currently authenticated finance owner.
"""

from jose import JWTError, jwt

from backend.app.core.security import (
    SECRET_KEY,
    ALGORITHM
)


def decode_access_token(token: str):
    """
    Decode a JWT access token.

    Returns:
        dict | None
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None