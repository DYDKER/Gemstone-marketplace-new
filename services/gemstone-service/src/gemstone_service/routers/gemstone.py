
from ..schemas import GemstoneCreate, GemstoneResponse, GemstoneUpdate
from ..database import get_session
from ..models import Gemstone

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


router = APIRouter(prefix="/gemstone", tags=["gemstone"])


@router.get("", response_model=list[GemstoneResponse])
async def read_gemstones(
        session: AsyncSession = Depends(get_session)
):
    result = await session.scalars(select(Gemstone))
    return result.all()


@router.get("/{gemstone_id}", response_model=GemstoneResponse, status_code=status.HTTP_200_OK)
async def read_gemstone(
        gemstone_id: int,
        session: AsyncSession = Depends(get_session)
):
    result = await session.get(Gemstone, gemstone_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gemstone not found",
        )

    return result


@router.post("", response_model=GemstoneResponse, status_code=status.HTTP_201_CREATED)
async def create_gemstone(
        gemstone_data: GemstoneCreate,
        session: AsyncSession = Depends(get_session)
):
    result = Gemstone(**gemstone_data.model_dump())

    session.add(result)
    await session.commit()
    await session.refresh(result)

    return result


@router.patch("/{gemstone_id}", response_model=GemstoneResponse, status_code=status.HTTP_200_OK)
async def update_gemstone(
        gemstone_id: int,
        gemstone_data: GemstoneUpdate,
        session: AsyncSession = Depends(get_session)
):
    result = await session.get(Gemstone, gemstone_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gemstone not found",
        )

    updated_gemstone = gemstone_data.model_dump(exclude_unset=True)

    for field, value in updated_gemstone.items():
        setattr(result, field, value)

    await session.commit()
    await session.refresh(result)

    return result


@router.delete("/{gemstone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gemstone(
        gemstone_id: int,
        session: AsyncSession = Depends(get_session)
):
    result = await session.get(Gemstone, gemstone_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gemstone not found",
        )

    await session.delete(result)
    await session.commit()
