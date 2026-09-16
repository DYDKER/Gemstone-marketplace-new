from datetime import datetime
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, Integer, String, func, true
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class GemstoneType(StrEnum):
    DIAMOND = 'Diamond'
    RUBY = 'Ruby'
    SAPPHIRE = 'Sapphire'


class Gemstone(Base):
    __tablename__ = 'gemstones'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(240), unique=True, nullable=False)
    gemstone_type: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    carat_weight: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(320), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean,default=True, server_default=true())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

