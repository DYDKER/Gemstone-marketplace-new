from .exceptions import StoneNotFoundError
from .repository import GemstoneRepository
from .schemas import GemstoneCreate, GemstoneResponse, GemstoneUpdate


class GemstoneService:
    def __init__(self, repository: GemstoneRepository):
        self.repository = repository

    async def get_gems(self) -> list[GemstoneResponse]:
        items = await self.repository.get_all()
        return [GemstoneResponse.model_validate(gem) for gem in items]

    async def get_gem(self, gemstone_id: int) -> GemstoneResponse:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        return GemstoneResponse.model_validate(gem)

    async def create_gem(self, gemstone_data: GemstoneCreate) -> GemstoneResponse:
        gem = await self.repository.create(**gemstone_data.model_dump())
        return GemstoneResponse.model_validate(gem)

    async def update_gem(self, gemstone_id: int, gemstone_data: GemstoneUpdate) -> GemstoneResponse:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        changes = gemstone_data.model_dump(exclude_unset=True)
        gem = await self.repository.update(gem, changes)
        return GemstoneResponse.model_validate(gem)

    async def delete_gem(self, gemstone_id: int) -> None:
        gem = await self.repository.get_by_id(gemstone_id)

        if gem is None:
            raise StoneNotFoundError()

        await self.repository.delete(gem)
