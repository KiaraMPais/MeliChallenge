from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session
from database import sql_connection
from uuid import UUID
from models import DBData
from core import AnalyzerEngine, decrypt_string

router = APIRouter()


@router.post("/{id}")
def scan(*, session: Session = Depends(sql_connection.get_session), id: UUID ):
    try:
        db_data = session.get_one(DBData, id)
        if db_data:
            connection_string = db_data.connection_string
            analyzer = AnalyzerEngine(decrypt_string(connection_string))
            return analyzer.classify_db_structure()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No database connection was found")

