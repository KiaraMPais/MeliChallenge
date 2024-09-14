from contextlib import asynccontextmanager

from fastapi import FastAPI
from database import sql_connection
from routes import app_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        sql_connection.create_db_and_tables()
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(app_router, prefix='/api')