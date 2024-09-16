from fastapi import APIRouter
from .database import router as connections_router
from .scan import router as scan_router
from .rule import router as rule_router

app_router = APIRouter(prefix="/v1")
connections_router.include_router(scan_router, prefix='/scan')
app_router.include_router(connections_router, prefix='/database', tags=['Database'])
app_router.include_router(rule_router, prefix='/rule', tags=['Rule'])