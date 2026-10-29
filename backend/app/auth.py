from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi import Depends, Header, HTTPException, status
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    GOOGLE_CLIENT_ID,
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    require_auth_configuration,
)
from app.db.models.user import User
from app.db.session import get_db


# API req/res models
class GoogleSignInRequest(BaseModel):
    id_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def verify_google_id_token(token: str) -> dict[str, object]:
    require_auth_configuration()
    try:
        claims = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except (ValueError, GoogleAuthError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google ID token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    if claims.get("email_verified") is not True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account email is not verified",
        )
    return claims


def create_access_token(user_id: str) -> str:
    require_auth_configuration()
    expires_at = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": user_id, "exp": expires_at},
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.removeprefix("Bearer ").strip()
    try:
        require_auth_configuration()
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
    except (jwt.InvalidTokenError, RuntimeError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    if not isinstance(user_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def sign_in_with_google(
    request: GoogleSignInRequest,
    db: Session,
) -> TokenResponse:
    claims = verify_google_id_token(request.id_token)
    google_id = claims.get("sub")
    email = claims.get("email")
    display_name = claims.get("name")

    if not isinstance(google_id, str) or not isinstance(email, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google ID token is missing required account details",
        )

    user = db.scalar(select(User).where(User.google_id == google_id))
    if user is None:
        user_by_email = db.scalar(select(User).where(User.email == email))
        if user_by_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account already exists for this email address",
            )
        user = User(
            id=str(uuid4()),
            google_id=google_id,
            email=email,
            display_name=display_name if isinstance(display_name, str) else None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return TokenResponse(access_token=create_access_token(user.id))
