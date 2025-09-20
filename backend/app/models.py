# backend/app/models.py
from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, sa_column_kwargs={"unique": True})
    hashed_password: str
    is_admin: bool = False

class Sweet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category: str
    price: float
    quantity: int = 0
