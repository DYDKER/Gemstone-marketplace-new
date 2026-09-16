from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[User]:
        result = await self.session.scalars(select(User))
        return list(result.all())

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, email: str, username: str) -> User:
        user = User(email=email, username=username)
        self.session.add(user)
        return await self.save(user)

    async def update(self, user: User, changes: dict[str, object]) -> User:
        for field, value in changes.items():
            setattr(user, field, value)

        return await self.save(user)

    async def save(self, user: User) -> User:
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
