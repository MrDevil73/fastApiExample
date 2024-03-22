from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import first_router
from database import create_tables, delete_tables
from script_add_values import mn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    await mn()
    #print("База готова")
    yield
    await delete_tables()
    #print("База очищена")


app = FastAPI(lifespan=lifespan)

app.include_router(first_router)
