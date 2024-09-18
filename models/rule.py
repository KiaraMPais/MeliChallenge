from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class RuleCreate(SQLModel):
    rule_name: str = Field(..., max_length=100)
    regex_pattern: str = Field(...)

class RuleUpdate(SQLModel):
    rule_name: Optional[str] = Field(max_length=100)
    regex_pattern: Optional[str]

class Rule(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    rule_name: str = Field(..., max_length=100)
    regex_pattern: str = Field(...)
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: Optional[datetime] = None