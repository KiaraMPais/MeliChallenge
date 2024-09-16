from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models import DBData, DBDataCreate, DBDataResponse, engine_map
from database import sql_connection
from core.encryption import encrypt_string

router = APIRouter()

@router.get("", response_model=list[DBDataResponse])
def get_connections(*, session: Session = Depends(sql_connection.get_session)):
    return session.exec(select(DBData))

@router.post("", response_model=DBDataResponse)
def new_connection(*, session: Session = Depends(sql_connection.get_session), connection: DBDataCreate):
    try:
        connection_string = f"{engine_map[connection.engine]}://{connection.username}:{connection.password}@{connection.host}:{connection.port}/{connection.database}"
        db_connection = DBData(friendly_name=connection.friendly_name, connection_string=encrypt_string(connection_string))
        session.add(db_connection)
        session.commit()
        session.refresh(db_connection)
        return db_connection
    except:
        pass

