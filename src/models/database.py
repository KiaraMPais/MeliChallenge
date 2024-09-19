from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Optional, Literal
from sqlmodel import Field, SQLModel


# Mapeo de motores de base de datos
engine_map = {
    "MySQL": "mysql+mysqlconnector",
    "PostgreSQL": "postgresql+psycopg2",
    "SQLite": "sqlite",
    "SQLServer": "mssql+pyodbc"
}

#Data Source Connections
class DBData(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    friendly_name: Optional[str]
    connection_string: str
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: Optional[datetime] = None

# Para poder ser flexibles con el motor, pero ser "user friendly" se mapeo el connector a un friendly name
class DBDataCreate(SQLModel):
    friendly_name: Optional[str]
    host: str
    port: int
    username: str
    password: str
    database: str
    engine: Literal["MySQL", "PostgreSQL", "SQLite", "SQLServer"]

class DBDataResponse(SQLModel):
    id: UUID
    friendly_name: Optional[str]
    created: datetime
    updated: Optional[datetime]

