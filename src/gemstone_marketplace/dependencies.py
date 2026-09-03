from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from gemstone_marketplace.database import get_session, settings
from gemstone_marketplace.exceptions import InvalidCredentialsError
from gemstone_marketplace.repositories.gemstones import GemstoneRepository
from gemstone_marketplace.repositories.users import UserRepository
from gemstone_marketplace.schemas import UserResponse
from gemstone_marketplace.security import PasswordManager, TokenManager
from gemstone_marketplace.services.auth import AuthService
from gemstone_marketplace.services.gemstones import GemstoneService
from gemstone_marketplace.services.users import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]

password_manager = PasswordManager()
token_manager = TokenManager(
    settings.jwt_secret_key.get_secret_value(),
    settings.access_token_expire_minutes,
)


def get_password_manager() -> PasswordManager:
    return password_manager


PasswordManagerDep = Annotated[PasswordManager, Depends(get_password_manager)]


def get_token_manager() -> TokenManager:
    return token_manager


TokenManagerDep = Annotated[TokenManager, Depends(get_token_manager)]


def get_auth_service(
    repository: UserRepositoryDep,
    password_service: PasswordManagerDep,
    token_service: TokenManagerDep,
) -> AuthService:
    return AuthService(repository, password_service, token_service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

bearer_scheme = HTTPBearer(auto_error=False)
BearerCredentialsDep = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]


async def get_current_user(
    credentials: BearerCredentialsDep,
    service: AuthServiceDep,
) -> UserResponse:
    if credentials is None:
        raise InvalidCredentialsError
    return await service.authenticate(credentials.credentials)


CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]


def get_gemstone_repository(session: SessionDep) -> GemstoneRepository:
    return GemstoneRepository(session)


GemstoneRepositoryDep = Annotated[
    GemstoneRepository,
    Depends(get_gemstone_repository),
]


def get_gemstone_service(repository: GemstoneRepositoryDep) -> GemstoneService:
    return GemstoneService(repository)


GemstoneServiceDep = Annotated[GemstoneService, Depends(get_gemstone_service)]
