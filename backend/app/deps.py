# backend/app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .database import get_session
from .crud import get_user_by_username
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET")
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(session, username)
    if not user:
        raise credentials_exception
    return user
