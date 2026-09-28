from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core import security
from core.config import settings
from core.rate_limit import rate_limit_dependency
from core.logging import logger
from api.deps import get_db
from models.user import User
from pydantic import BaseModel, EmailStr, field_validator

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str = ""

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

@router.post("/login", response_model=Token, dependencies=[Depends(rate_limit_dependency(requests_per_minute=20))])
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.user_id, role=user.role, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit_dependency(requests_per_minute=10))])
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> Token:
    """
    Register a new user account and return an access token.
    """
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists."
        )
    
    user = User(
        email=request.email,
        hashed_password=security.get_password_hash(request.password),
        display_name=request.name or request.email.split("@")[0],
        role="USER",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"New user registered: {user.email}", extra={"endpoint": "/auth/register"})
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.user_id, role=user.role, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )
