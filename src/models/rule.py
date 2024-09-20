from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


# Value Rule lo usamos para las reglas que se basan en un valor para sacar el patron.

class RuleCreate(SQLModel):
    rule_name: str = Field(..., max_length=100)
    regex_pattern: str = Field(...)
    is_value_rule: bool = Field(default=False)

class RuleUpdate(SQLModel):
    rule_name: Optional[str] = Field(max_length=100)
    regex_pattern: Optional[str]
    is_value_rule: bool = Field(default=False)

class Rule(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    rule_name: str = Field(..., max_length=100)
    regex_pattern: str = Field(...)
    is_value_rule: bool = Field(default=False)
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: Optional[datetime] = None