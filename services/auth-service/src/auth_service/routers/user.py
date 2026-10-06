from fastapi import APIRouter, Depends, status

from ..dependencies import get_user_service
from ..schemas import UserCreate, UserResponse, UserUpdate
from ..service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def read_users(service: UserService = Depends(get_user_service)) -> list[UserResponse]:
    return await service.get_users()


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, service: UserService = Depends(get_user_service)) -> UserResponse:
    return await service.get_user(user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, service: UserService = Depends(get_user_service)) -> UserResponse:
    return await service.create_user(user_data)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, service: UserService = Depends(get_user_service)) -> UserResponse:
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    await service.delete_user(user_id)
