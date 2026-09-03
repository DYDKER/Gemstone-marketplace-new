from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from gemstone_marketplace.exceptions import UserAlreadyExistsError
from gemstone_marketplace.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> Sequence[User]:
        users = await self.session.scalars(select(User))
        return users.all()

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        return await self.session.scalar(select(User).where(User.email == email))

    async def create(self, data: dict[str, object]) -> User:
        user = User(**data)
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise UserAlreadyExistsError from error
        await self.session.refresh(user)
        return user

    async def update(
        self,
        user_id: int,
        data: dict[str, object],
    ) -> User | None:
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        for field, value in data.items():
            setattr(user, field, value)

        try:
            await self.session.commit()
        except IntegrityError as error:
            await self.session.rollback()
            raise UserAlreadyExistsError from error
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user is None:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True
