from fastapi import APIRouter, HTTPException, Depends
from mysql.connector import DATETIME
from sqlmodel import Session, select
from database import sql_connection
from models import Rule, RuleCreate, RuleUpdate
from core import load_classification_rules
from datetime import datetime

router = APIRouter()


"""Obtener todas las reglas de clasificación de la base de datos."""
@router.get("", response_model=list[Rule])
def get_rules(*, session: Session = Depends(sql_connection.get_session)):
    select_query = select(Rule)
    result = session.exec(select_query)
    return result.fetchall()


"""Agregar nuevas reglas de clasificación a la base de datos."""
@router.post("", response_model=Rule)
def create_rule(*, session: Session = Depends(sql_connection.get_session), rule: RuleCreate):
    try:
        new_rule = Rule.model_validate(rule)
        session.add(new_rule)
        session.commit()
        session.refresh(new_rule)

        # Refresh a la lista de reglas de clasificación
        load_classification_rules()

        return new_rule
    except:
        raise HTTPException(status_code=400, detail="Error adding rule")



"""Actualizar una regla existente en la base de datos."""
@router.put("/{rule_id}", status_code=204)
def update_rule(*, session: Session = Depends(sql_connection.get_session), rule_id: int, rule: RuleUpdate):
    select_query = select(Rule).where(Rule.id == rule_id)
    result = session.exec(select_query)
    existing_rule = result.one()

    existing_rule.rule_name = rule.rule_name
    existing_rule.regex_pattern = rule.regex_pattern
    existing_rule.updated = datetime.now(DATETIME.UTC)

    session.add(existing_rule)
    session.commit()

    # Refresh a la lista de reglas de clasificación
    load_classification_rules()

    if not existing_rule:
        raise HTTPException(status_code=404, detail="Rule not found")


"""Eliminar una regla de clasificación de la base de datos."""
@router.delete("/{rule_id}", status_code=204)
def delete_rule(*, session: Session = Depends(sql_connection.get_session), rule_id: int):
    try:
        query = select(Rule).where(Rule.id == rule_id)
        results = session.exec(query)
        rule = results.one()
        session.delete(rule)
        session.commit()
        return
    except:
        raise HTTPException(status_code=404, detail="Rule not found")


