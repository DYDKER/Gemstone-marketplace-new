from fastapi import Request
from fastapi.responses import JSONResponse

from gemstone_marketplace.exceptions import (
    InvalidCredentialsError,
    StoneAlreadyExistsError,
    StoneNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


async def user_not_found_handler(
    request: Request,
    exc: UserNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"},
    )


async def stone_not_found_handler(
    request: Request,
    exc: StoneNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": "Stone not found"},
    )


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "User with this email or username already exists"},
    )


async def stone_already_exists_handler(
    request: Request,
    exc: StoneAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": "Stone with this name already exists"},
    )


async def invalid_credentials_handler(
    request: Request,
    exc: InvalidCredentialsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={"detail": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"},
    )
