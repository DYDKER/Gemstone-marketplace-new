from fastapi import APIRouter, status

from gemstone_marketplace.dependencies import GemstoneServiceDep
from gemstone_marketplace.schemas import (
    GemstoneCreate,
    GemstoneResponse,
    GemstoneUpdate,
)

router = APIRouter(prefix="/gems", tags=["gems"])


@router.get("", response_model=list[GemstoneResponse])
async def read_gemstones(service: GemstoneServiceDep):
    return await service.get_gemstones()


@router.get("/{gemstone_id}", response_model=GemstoneResponse)
async def read_gemstone(gemstone_id: int, service: GemstoneServiceDep):
    return await service.get_gemstone(gemstone_id)


@router.post(
    "",
    response_model=GemstoneResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_gemstone(
    gemstone_data: GemstoneCreate,
    service: GemstoneServiceDep,
):
    return await service.create_gemstone(gemstone_data)


@router.patch("/{gemstone_id}", response_model=GemstoneResponse)
async def update_gemstone(
    gemstone_id: int,
    gemstone_data: GemstoneUpdate,
    service: GemstoneServiceDep,
):
    return await service.update_gemstone(
        gemstone_id,
        gemstone_data,
    )


@router.delete("/{gemstone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gemstone(gemstone_id: int, service: GemstoneServiceDep):
    await service.delete_gemstone(gemstone_id)
