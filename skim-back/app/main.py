from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import user
from app.database import Base, engine

app = FastAPI()

app.include_router(user.ROUTER, prefix="/users")
