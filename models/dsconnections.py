from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

def datetime_now() -> datetime:
    return datetime.now(timezone.utc)

#Data Source Connections
class DSConnections(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    friendly_name: Optional[str]
    connection_string: str
    created: datetime = Field(default_factory=datetime_now)
    updated: Optional[datetime]
