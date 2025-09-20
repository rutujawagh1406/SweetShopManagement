# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    admin_secret: Optional[str] = None

class LoginData(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    is_admin: bool

class SweetCreate(BaseModel):
    name: str
    category: str
    price: float
    quantity: int = 0

class SweetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None

class QuantityAction(BaseModel):
    quantity: int = 1
