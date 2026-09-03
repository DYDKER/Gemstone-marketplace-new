from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

from gemstone_marketplace.exceptions import InvalidCredentialsError

JWT_ALGORITHM = "HS256"


class PasswordManager:
    def __init__(self) -> None:
        self.password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            return self.password_hash.verify(password, hashed_password)
        except UnknownHashError:
            return False


class TokenManager:
    def __init__(self, secret_key: str, expire_minutes: int) -> None:
        self.secret_key = secret_key
        self.expire_minutes = expire_minutes

    def create_access_token(self, user_id: int) -> str:
        expires_at = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
        return jwt.encode(
            {"sub": str(user_id), "exp": expires_at},
            self.secret_key,
            algorithm=JWT_ALGORITHM,
        )

    def get_user_id(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[JWT_ALGORITHM],
            )
            user_id = int(payload["sub"])
            if user_id <= 0:
                raise ValueError
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError) as error:
            raise InvalidCredentialsError from error

        return user_id
