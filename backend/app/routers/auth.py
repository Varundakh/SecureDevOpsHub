from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import create_access_token, get_current_user, hash_password, security, verify_password
from app.models import create_user, get_user_by_email
from app.schemas import TokenResponse, UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: UserRegister) -> TokenResponse:
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = create_user(payload.email, hash_password(payload.password), payload.role)
    token = create_access_token(user["email"])
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin) -> TokenResponse:
    user = get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user["email"])
    return TokenResponse(access_token=token)
