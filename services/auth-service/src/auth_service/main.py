from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import UserNotFoundError
from .routers.user import router

app = FastAPI()


async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "User not found"})


app.add_exception_handler(UserNotFoundError, user_not_found_handler)
app.include_router(router)
