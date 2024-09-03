from datetime import datetime

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    category: str
    username: str


class Spend(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)
    amount: float
    description: str
    category: str
    spendDate: datetime
    currency: str


class SpendAdd(BaseModel):
    amount: float
    description: str
    category: str
    spendDate: str
    currency: str