from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session

from .repository import GemstoneRepository
from .service import GemstoneService


def get_gemstone_repository(session: AsyncSession = Depends(get_session)) -> GemstoneRepository:
    return GemstoneRepository(session)


def get_gemstone_service(repository: GemstoneRepository = Depends(get_gemstone_repository)) -> GemstoneService:
    return GemstoneService(repository)
