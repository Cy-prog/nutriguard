from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from uuid import UUID

from core.config import settings
from models.base import Base
from models.user import User
from core.database import engine, get_db, SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except (JWTError, ValidationError):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
    user = db.query(User).filter(User.user_id == UUID(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

def get_current_clinical_reviewer(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in ("CLINICAL_REVIEWER", "ADMIN"):
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user

def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user
