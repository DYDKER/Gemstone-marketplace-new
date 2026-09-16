from .exceptions import UserNotFoundError
from .repository import UserRepository
from .schemas import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_users(self) -> list[UserResponse]:
        items = await self.repository.get_all()
        return [UserResponse.model_validate(user) for user in items]

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        return UserResponse.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = await self.repository.create(email=user_data.email, username=user_data.username)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        changes = user_data.model_dump(exclude_unset=True)
        user = await self.repository.update(user, changes)
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        await self.repository.delete(user)
