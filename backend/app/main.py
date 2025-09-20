# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Optional
from .database import create_db_and_tables, get_session
from . import schemas, crud, auth
from .deps import get_current_user
from sqlmodel import select
from .models import Sweet, User
import os

from fastapi.middleware.cors import CORSMiddleware

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "ADMIN123")

app = FastAPI(title="Sweet Shop Management")

# CORS - allow frontend at port 3000 (Vite default)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Auth
@app.post("/api/auth/register")
def register(user: schemas.UserCreate, session=Depends(get_session)):
    existing = crud.get_user_by_username(session, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    is_admin = bool(user.admin_secret and user.admin_secret == ADMIN_SECRET)
    db_user = crud.create_user(session, user.username, user.password, is_admin)
    return {"msg":"User created", "username": db_user.username, "is_admin": db_user.is_admin}

@app.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(data: schemas.LoginData, session=Depends(get_session)):
    user = crud.authenticate_user(session, data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = auth.create_access_token({"sub": user.username, "user_id": user.id, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "username": user.username, "is_admin": user.is_admin}

# Sweets endpoints
@app.post("/api/sweets", response_model=schemas.SweetCreate)
def add_sweet(sweet: schemas.SweetCreate, current_user: User = Depends(get_current_user), session=Depends(get_session)):
    db_sweet = crud.create_sweet(session, sweet.name, sweet.category, sweet.price, sweet.quantity)
    return db_sweet

@app.get("/api/sweets", response_model=List[Sweet])
def list_sweets(session=Depends(get_session)):
    return session.exec(select(Sweet)).all()

@app.get("/api/sweets/search", response_model=List[Sweet])
def search_sweets(name: Optional[str] = None, category: Optional[str] = None,
                  min_price: Optional[float] = None, max_price: Optional[float] = None,
                  session=Depends(get_session)):
    query = select(Sweet)
    if name:
        query = query.where(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.where(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.where(Sweet.price >= min_price)
    if max_price is not None:
        query = query.where(Sweet.price <= max_price)
    return session.exec(query).all()

@app.put("/api/sweets/{sweet_id}", response_model=Sweet)
def update_sweet(sweet_id: int, payload: schemas.SweetUpdate, current_user: User = Depends(get_current_user),
                 session=Depends(get_session)):
    db_sweet = session.get(Sweet, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(db_sweet, key, value)
    session.add(db_sweet)
    session.commit()
    session.refresh(db_sweet)
    return db_sweet

@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(sweet_id: int, current_user: User = Depends(get_current_user), session=Depends(get_session)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    db_sweet = session.get(Sweet, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    session.delete(db_sweet)
    session.commit()
    return {"msg": "Deleted"}

@app.post("/api/sweets/{sweet_id}/purchase", response_model=Sweet)
def purchase_sweet(sweet_id: int, action: schemas.QuantityAction, current_user: User = Depends(get_current_user),
                   session=Depends(get_session)):
    db_sweet = session.get(Sweet, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if action.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be >= 1")
    if db_sweet.quantity < action.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    db_sweet.quantity -= action.quantity
    session.add(db_sweet)
    session.commit()
    session.refresh(db_sweet)
    return db_sweet

@app.post("/api/sweets/{sweet_id}/restock", response_model=Sweet)
def restock_sweet(sweet_id: int, action: schemas.QuantityAction, current_user: User = Depends(get_current_user),
                  session=Depends(get_session)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    db_sweet = session.get(Sweet, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    if action.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be >= 1")
    db_sweet.quantity += action.quantity
    session.add(db_sweet)
    session.commit()
    session.refresh(db_sweet)
    return db_sweet
