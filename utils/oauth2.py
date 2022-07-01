from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import timedelta, datetime
from typing import Optional
from sqlmodel import Session, select
from database.db_connect import get_session
from schemas import User, UserOutput

from jose import JWSError, jwt
from decouple import config

URL_PREFIX = "/auth"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{URL_PREFIX}/token")

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = generate_expire_date(expire_delta)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def generate_expire_date(expire_delta: Optional[timedelta] = None):
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    return expire


def access_user_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWSError:
        raise credentials_exception

    query = select(User).where(username == username)
    result = db.exec(query).first()
    if not result:
        raise credentials_exception
    return result
