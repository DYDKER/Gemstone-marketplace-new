from fastapi import APIRouter, Depends, status

from ..dependencies import get_gemstone_service
from ..schemas import GemstoneCreate, GemstoneResponse, GemstoneUpdate
from ..service import GemstoneService

router = APIRouter(prefix="/gems", tags=["gems"])


@router.get("", response_model=list[GemstoneResponse])
async def read_gemstones(service: GemstoneService = Depends(get_gemstone_service)) -> list[GemstoneResponse]:
    return await service.get_gems()


@router.get("/{gemstone_id}", response_model=GemstoneResponse)
async def read_gemstone(gemstone_id: int, service: GemstoneService = Depends(get_gemstone_service)) -> GemstoneResponse:
    return await service.get_gem(gemstone_id)


@router.post("", response_model=GemstoneResponse, status_code=status.HTTP_201_CREATED)
async def create_gemstone(gemstone_data: GemstoneCreate, service: GemstoneService = Depends(get_gemstone_service)) -> GemstoneResponse:
    return await service.create_gem(gemstone_data)


@router.patch("/{gemstone_id}", response_model=GemstoneResponse)
async def update_gemstone(gemstone_id: int, gemstone_data: GemstoneUpdate, service: GemstoneService = Depends(get_gemstone_service)) -> GemstoneResponse:
    return await service.update_gem(gemstone_id, gemstone_data)


@router.delete("/{gemstone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gemstone(gemstone_id: int, service: GemstoneService = Depends(get_gemstone_service)) -> None:
    await service.delete_gem(gemstone_id)
