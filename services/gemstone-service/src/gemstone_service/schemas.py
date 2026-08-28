from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .models import GemstoneType


class GemstoneCreate(BaseModel):
    name: str
    gemstone_type: GemstoneType
    price: int
    carat_weight: int
    description: str | None = None
    is_available: bool = True


class GemstoneUpdate(BaseModel):
    name: str | None = None
    gemstone_type: GemstoneType | None = None
    price: int | None = None
    carat_weight: int | None = None
    description: str | None = None
    is_available: bool | None = None


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
