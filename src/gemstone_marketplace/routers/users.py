from fastapi import APIRouter, status

from gemstone_marketplace.dependencies import (
    AuthServiceDep,
    CurrentUserDep,
    UserServiceDep,
)
from gemstone_marketplace.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def read_users(service: UserServiceDep):
    return await service.get_users()


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: CurrentUserDep):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, service: UserServiceDep):
    return await service.get_user(user_id)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, service: AuthServiceDep):
    return await service.register(user_data)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    service: UserServiceDep,
):
    return await service.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserServiceDep):
    await service.delete_user(user_id)
