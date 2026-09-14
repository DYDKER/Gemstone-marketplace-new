from fastapi import FastAPI

from .routers.gemstone import router

app = FastAPI()


app.include_router(router)