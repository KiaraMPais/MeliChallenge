from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import DSConnection, DSConnectionCreate, DSConnectionResponse, engine_map
from database import sql_connection
from core.encryption import encrypt_string

router = APIRouter()

@router.post("", response_model=DSConnectionResponse)
def new_connection(*, session: Session = Depends(sql_connection.get_session), connection: DSConnectionCreate):
    try:
        connection_string = f"{engine_map[connection.engine]}://{connection.username}:{connection.password}@{connection.host}:{connection.port}/{connection.database}"
        db_connection = DSConnection(friendly_name=connection.friendly_name, connection_string=encrypt_string(connection_string))
        session.add(db_connection)
        session.commit()
        session.refresh(db_connection)
        return db_connection
    except:
        pass

