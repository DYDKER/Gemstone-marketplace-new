from gemstone_marketplace.exceptions import StoneNotFoundError
from gemstone_marketplace.repositories.gemstones import GemstoneRepository
from gemstone_marketplace.schemas import (
    GemstoneCreate,
    GemstoneResponse,
    GemstoneUpdate,
)


class GemstoneService:
    def __init__(self, repository: GemstoneRepository):
        self.repository = repository

    async def get_gemstones(self) -> list[GemstoneResponse]:
        gemstones = await self.repository.get_all()
        return [GemstoneResponse.model_validate(gemstone) for gemstone in gemstones]

    async def get_gemstone(self, gemstone_id: int) -> GemstoneResponse:
        gemstone = await self.repository.get_by_id(gemstone_id)
        if gemstone is None:
            raise StoneNotFoundError
        return GemstoneResponse.model_validate(gemstone)

    async def create_gemstone(
        self,
        gemstone_data: GemstoneCreate,
    ) -> GemstoneResponse:
        gemstone = await self.repository.create(gemstone_data.model_dump())
        return GemstoneResponse.model_validate(gemstone)

    async def update_gemstone(
        self,
        gemstone_id: int,
        gemstone_data: GemstoneUpdate,
    ) -> GemstoneResponse:
        gemstone = await self.repository.update(
            gemstone_id,
            gemstone_data.model_dump(exclude_unset=True),
        )
        if gemstone is None:
            raise StoneNotFoundError
        return GemstoneResponse.model_validate(gemstone)

    async def delete_gemstone(self, gemstone_id: int) -> None:
        deleted = await self.repository.delete(gemstone_id)
        if not deleted:
            raise StoneNotFoundError
