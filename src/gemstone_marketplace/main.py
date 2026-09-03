from fastapi import FastAPI

from gemstone_marketplace.exception_handlers import (
    stone_already_exists_handler,
    stone_not_found_handler,
    user_already_exists_handler,
    user_not_found_handler,
)
from gemstone_marketplace.exceptions import (
    StoneAlreadyExistsError,
    StoneNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from gemstone_marketplace.routers.gemstones import router as gemstones_router
from gemstone_marketplace.routers.users import router as users_router

app = FastAPI(title="Gemstone Marketplace")

app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.add_exception_handler(StoneNotFoundError, stone_not_found_handler)
app.add_exception_handler(UserAlreadyExistsError, user_already_exists_handler)
app.add_exception_handler(StoneAlreadyExistsError, stone_already_exists_handler)

app.include_router(users_router)
app.include_router(gemstones_router)
