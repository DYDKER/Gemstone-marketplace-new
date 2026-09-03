from fastapi import APIRouter, status

from gemstone_marketplace.dependencies import AuthServiceDep
from gemstone_marketplace.schemas import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_data: UserCreate, service: AuthServiceDep):
    return await service.register(user_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, service: AuthServiceDep):
    return await service.login(login_data)
