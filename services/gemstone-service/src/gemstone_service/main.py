from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import StoneNotFoundError
from .routers.gemstone import router

app = FastAPI()


async def stone_not_found_handler(request: Request, exc: StoneNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": "Gemstone not found"})


app.add_exception_handler(StoneNotFoundError, stone_not_found_handler)
app.include_router(router)
