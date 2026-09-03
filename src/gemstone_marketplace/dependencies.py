from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from gemstone_marketplace.database import get_session
from gemstone_marketplace.repositories.gemstones import GemstoneRepository
from gemstone_marketplace.repositories.users import UserRepository
from gemstone_marketplace.services.gemstones import GemstoneService
from gemstone_marketplace.services.users import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_user_service(repository: UserRepositoryDep) -> UserService:
    return UserService(repository)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_gemstone_repository(session: SessionDep) -> GemstoneRepository:
    return GemstoneRepository(session)


GemstoneRepositoryDep = Annotated[
    GemstoneRepository,
    Depends(get_gemstone_repository),
]


def get_gemstone_service(repository: GemstoneRepositoryDep) -> GemstoneService:
    return GemstoneService(repository)


GemstoneServiceDep = Annotated[GemstoneService, Depends(get_gemstone_service)]
