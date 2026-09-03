from gemstone_marketplace.exceptions import InvalidCredentialsError
from gemstone_marketplace.repositories.users import UserRepository
from gemstone_marketplace.schemas import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from gemstone_marketplace.security import PasswordManager, TokenManager


class AuthService:
    def __init__(
        self,
        repository: UserRepository,
        password_manager: PasswordManager,
        token_manager: TokenManager,
    ) -> None:
        self.repository = repository
        self.password_manager = password_manager
        self.token_manager = token_manager

    async def register(self, user_data: UserCreate) -> UserResponse:
        data = user_data.model_dump(exclude={"password"})
        data["hashed_password"] = self.password_manager.hash(user_data.password)
        user = await self.repository.create(data)
        return UserResponse.model_validate(user)

    async def login(self, login_data: LoginRequest) -> TokenResponse:
        user = await self.repository.get_by_email(str(login_data.email))
        if user is None or not self.password_manager.verify(
            login_data.password,
            user.hashed_password,
        ):
            raise InvalidCredentialsError

        if not user.is_active:
            raise InvalidCredentialsError

        token = self.token_manager.create_access_token(user.id)
        return TokenResponse(access_token=token)

    async def authenticate(self, token: str) -> UserResponse:
        user_id = self.token_manager.get_user_id(token)
        user = await self.repository.get_by_id(user_id)
        if user is None or not user.is_active:
            raise InvalidCredentialsError
        return UserResponse.model_validate(user)
