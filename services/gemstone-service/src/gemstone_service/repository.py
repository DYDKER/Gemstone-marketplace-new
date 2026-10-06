from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from .exceptions import ImageSaveRejectedError
from .models import Gemstone


class GemstoneRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Gemstone]:
        result = await self.session.scalars(select(Gemstone))
        return list(result.all())

    async def get_by_id(self, gemstone_id: int) -> Gemstone | None:
        return await self.session.get(Gemstone, gemstone_id)

    async def create(self, name: str, gemstone_type: str, price: int, carat_weight: int, description: str | None = None, is_available: bool = True) -> Gemstone:
        gem = Gemstone(name=name, gemstone_type=gemstone_type, price=price, carat_weight=carat_weight, description=description, is_available=is_available)
        self.session.add(gem)
        return await self.save(gem)

    async def update(self, gem: Gemstone, changes: dict[str, object]) -> Gemstone:
        for field, value in changes.items():
            setattr(gem, field, value)

        return await self.save(gem)

    async def save(self, gem: Gemstone) -> Gemstone:
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise

        await self.session.refresh(gem)
        return gem

    async def delete(self, gem: Gemstone) -> None:
        await self.session.delete(gem)
        await self.session.commit()

    async def set_image_key(self, gem: Gemstone, key: str) -> Gemstone:
        gem.image_key = key

        try:
            await self.session.flush()
        except SQLAlchemyError as exc:
            await self.session.rollback()
            raise ImageSaveRejectedError() from exc

        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise

        return gem
