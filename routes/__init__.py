from fastapi import APIRouter
from .database import router as connections_router

app_router = APIRouter(prefix="/v1")
app_router.include_router(connections_router, prefix='/database', tags=['database'])