from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

UserEmail = Annotated[EmailStr, Field(max_length=320)]
Username = Annotated[str, Field(min_length=1, max_length=240)]
GemstoneName = Annotated[str, Field(min_length=1, max_length=240)]
GemstoneDescription = Annotated[str, Field(max_length=320)]
PositiveInteger = Annotated[int, Field(gt=0)]
Password = Annotated[str, Field(min_length=8, max_length=128)]


class GemstoneType(StrEnum):
    DIAMOND = "Diamond"
    RUBY = "Ruby"
    SAPPHIRE = "Sapphire"


class UserCreate(BaseModel):
    email: UserEmail
    username: Username
    password: Password


class UserUpdate(BaseModel):
    email: UserEmail | None = None
    username: Username | None = None
    is_active: bool | None = None

    @field_validator("email", "username", "is_active")
    @classmethod
    def reject_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("Field cannot be null")
        return value


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: UserEmail
    password: Password


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class GemstoneCreate(BaseModel):
    name: GemstoneName
    gemstone_type: GemstoneType
    price: PositiveInteger
    carat_weight: PositiveInteger
    description: GemstoneDescription | None = None
    is_available: bool = True


class GemstoneUpdate(BaseModel):
    name: GemstoneName | None = None
    gemstone_type: GemstoneType | None = None
    price: PositiveInteger | None = None
    carat_weight: PositiveInteger | None = None
    description: GemstoneDescription | None = None
    is_available: bool | None = None

    @field_validator(
        "name",
        "gemstone_type",
        "price",
        "carat_weight",
        "is_available",
    )
    @classmethod
    def reject_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("Field cannot be null")
        return value


class GemstoneResponse(BaseModel):
    id: int
    name: str
    gemstone_type: GemstoneType
    price: int
    carat_weight: int
    description: str | None
    is_available: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
