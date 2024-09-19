from sqlalchemy.orm import Relationship
from sqlmodel import SQLModel, Field, JSON
from typing import Optional
from datetime import datetime
from uuid import UUID


# 7df13a10-8a41-4e11-ba8f-b6930f1ba81b

class ScanResultResponse(SQLModel):
    id: int
    database_id: UUID
    data: dict
    created: datetime

class ScanResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    database_id: UUID = Relationship(foreign_keys="dbdata.id")
    data: dict = Field(sa_type=JSON)
    created: datetime = Field(default_factory=datetime.utcnow)


