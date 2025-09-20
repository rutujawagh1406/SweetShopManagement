# backend/app/crud.py
from sqlmodel import select
from .models import User, Sweet
from .auth import get_password_hash, verify_password
from sqlmodel import Session

def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()

def create_user(session: Session, username: str, password: str, is_admin: bool=False):
    user = User(username=username, hashed_password=get_password_hash(password), is_admin=is_admin)
    session.add(user); session.commit(); session.refresh(user)
    return user

def authenticate_user(session: Session, username: str, password: str):
    user = get_user_by_username(session, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_sweet(session: Session, name: str, category: str, price: float, quantity: int=0):
    sweet = Sweet(name=name, category=category, price=price, quantity=quantity)
    session.add(sweet); session.commit(); session.refresh(sweet)
    return sweet

def get_sweet(session: Session, sweet_id: int):
    return session.get(Sweet, sweet_id)
