from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from gemstone_marketplace.exceptions import StoneAlreadyExistsError
from gemstone_marketplace.models import Gemstone


class GemstoneRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[Gemstone]:
        gemstones = await self.session.scalars(select(Gemstone))
        return gemstones.all()

    async def get_by_id(self, gemstone_id: int) -> Gemstone | None:
        return await self.session.get(Gemstone, gemstone_id)

    async def create(self, data: dict[str, object]) -> Gemstone:
        gemstone = Gemstone(**data)
        self.session.add(gemstone)
        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise StoneAlreadyExistsError from error
        await self.session.refresh(gemstone)
        return gemstone

    async def update(
        self,
        gemstone_id: int,
        data: dict[str, object],
    ) -> Gemstone | None:
        gemstone = await self.get_by_id(gemstone_id)
        if gemstone is None:
            return None

        for field, value in data.items():
            setattr(gemstone, field, value)

        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise StoneAlreadyExistsError from error
        await self.session.refresh(gemstone)
        return gemstone

    async def delete(self, gemstone_id: int) -> bool:
        gemstone = await self.get_by_id(gemstone_id)
        if gemstone is None:
            return False

        await self.session.delete(gemstone)
        await self.session.commit()
        return True
