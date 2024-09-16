from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import sql_connection
from models import Rule, RuleCreate, RuleUpdate
from core import load_classification_rules

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
"""
@router.put("/{id}")
def update_rule(*, session: Session = Depends(sql_connection.get_session), id: UUID, rule: RuleUpdate):
    select_query = select(Rule).where(Rule.id == id)
    result = session.exec(select_query)
    existing_rule = result.first()
    if not existing_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    


@router.delete("/{id}")
def delete_rule(rule_name: str):

    classification_rules_table = get_classification_rules_table()

    delete_query = delete(classification_rules_table).where(
        classification_rules_table.c.rule_name == rule_name
    )

    with rules_engine.connect() as conn:
        result = conn.execute(delete_query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Rule not found")
        return {"message": "Rule deleted successfully"}
"""
"""Eliminar una regla de clasificación de la base de datos."""