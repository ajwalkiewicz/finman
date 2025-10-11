import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .crud import get_user_by_username
from .database import User, get_session

# Security configuration
load_dotenv("/app/data/.env")

_ALGORITHM = "HS256"
_ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = os.getenv("SECRET_KEY", None)
if SECRET_KEY is None or len(SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY must be set and at least 32 characters long")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Secret(BaseModel):
    key: str
    algorithm: str
    access_token_expire_minutes: int


secret = Secret(
    key=SECRET_KEY,
    algorithm=os.getenv("ALGORITHM", _ALGORITHM),
    access_token_expire_minutes=int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", _ACCESS_TOKEN_EXPIRE_MINUTES)
    ),
)


class Token(BaseModel):
    # model_config = ConfigDict(alias_generator=to_camel)

    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=secret.access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret.key, algorithm=secret.algorithm)
    return encoded_jwt


async def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret.key, algorithms=[secret.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    token_data = TokenData(username=username)
    if token_data.username is None:
        raise credentials_exception

    user = get_user_by_username(session, token_data.username)
    if user is None:
        raise credentials_exception
    return user
