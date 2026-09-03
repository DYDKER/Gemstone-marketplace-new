from gemstone_marketplace.exceptions import UserNotFoundError
from gemstone_marketplace.repositories.users import UserRepository
from gemstone_marketplace.schemas import UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_users(self) -> list[UserResponse]:
        users = await self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError
        return UserResponse.model_validate(user)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = await self.repository.create(user_data.model_dump())
        return UserResponse.model_validate(user)

    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
    ) -> UserResponse:
        user = await self.repository.update(
            user_id,
            user_data.model_dump(exclude_unset=True),
        )
        if user is None:
            raise UserNotFoundError
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        deleted = await self.repository.delete(user_id)
        if not deleted:
            raise UserNotFoundError
