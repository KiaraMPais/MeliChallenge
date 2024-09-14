from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, Literal
from sqlmodel import Field, SQLModel

def datetime_now() -> datetime:
    return datetime.now(timezone.utc)


engine_map = {
    "MySQL": "mysql+mysqlconnector",
    "PostgreSQL": "postgresql+psycopg2",
    "SQLite": "sqlite",
    "SQLServer": "mssql+pyodbc"
}

#Data Source Connections
class DSConnection(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    friendly_name: Optional[str]
    connection_string: str
    created: datetime = Field(default_factory=datetime_now)
    updated: Optional[datetime]


class DSConnectionCreate(SQLModel):
    friendly_name: Optional[str]
    host: str
    port: int
    username: str
    password: str
    database: str
    engine: Literal["MySQL", "PostgreSQL", "SQLite", "SQLServer"]


class DSConnectionResponse(SQLModel):
    id: UUID
    friendly_name: Optional[str]
    created: datetime
    updated: Optional[datetime]

