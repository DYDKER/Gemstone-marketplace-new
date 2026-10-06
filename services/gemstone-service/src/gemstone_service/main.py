from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import InvalidImageError, StoneNotFoundError, StoneImageNotFoundError
from .routers.gemstone import router

app = FastAPI()


async def stone_not_found_handler(request: Request, exc: StoneNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Gemstone not found"})


async def invalid_image_handler(request: Request, exc: InvalidImageError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


async def stone_image_not_found_handler(request: Request, exc: StoneImageNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Gemstone image not found"})


app.add_exception_handler(InvalidImageError, invalid_image_handler)
app.add_exception_handler(StoneNotFoundError, stone_not_found_handler)
app.add_exception_handler(StoneImageNotFoundError, stone_image_not_found_handler)
app.include_router(router)
