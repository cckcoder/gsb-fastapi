from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database.db_connect import get_session
from schemas import UserOutput, User, Token
from sqlmodel import Session, select

from utils.helper_exception import UnauthorizeException
from utils.oauth2 import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)
):
    statement = select(User).where(User.username == form_data.username)
    user = db.exec(statement).first()
    if user and user.verify_password(form_data.password):
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise UnauthorizeException()
