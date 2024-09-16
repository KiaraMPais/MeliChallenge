from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from database import sql_connection
from uuid import UUID
from models import DBData, ScanResult, ScanResultResponse
from core import AnalyzerEngine, decrypt_string

router = APIRouter()

""" Una alternativa a guardar el resultado del escaneo directamente como JSON hubiese sido guardar una entrada
    por cada campo analizado. Pero ahi es mas trabajo mantener una consistencia en los datos por si la DB se modifica.
    Por esto se guardo directamente todo el JSON con fecha, ya que su peso es despreciable, y cumple con el objetivo.
"""
@router.post("/{id}", status_code=201)
def scan(*, session: Session = Depends(sql_connection.get_session), id: UUID ):
    try:
        db_data = session.get_one(DBData, id)
        if db_data:
            scan = ScanResult()
            connection_string = db_data.connection_string
            analyzer = AnalyzerEngine(decrypt_string(connection_string))
            scan.database_id = id
            scan.data = analyzer.classify_db_structure()
            session.add(scan)
            session.commit()
        return

    except NoResultFound:
        raise HTTPException(status_code=404, detail="No database connection was found")


@router.get("/{id}", response_model=ScanResultResponse, status_code=200)
def get_scan(*, session: Session = Depends(sql_connection.get_session), id: UUID):
    try:
        statement = (
            select(ScanResult)
            .where(ScanResult.database_id == id)
            .order_by(ScanResult.created.desc())
            .limit(1)
        )
        result = session.exec(statement).first()
        return result
    except NoResultFound:
        raise HTTPException(status_code=404, detail="No scan result was found")

