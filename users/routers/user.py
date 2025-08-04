import os
import base64

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from dotenv import load_dotenv

from users.db.models import User
from users.schemas.schemas import UserCreate
from load_env import secret_key
from common.utils import decode_token
from dependencies import get_db



users_router = APIRouter(prefix="/users")

@users_router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='User already registred.')

    data = user.model_dump()
    data.update({"role": "USER"})
    token = jwt.encode(data, secret_key, algorithm='HS256')

    db_user = User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return token


@users_router.get("/check-info")
async def check_info_from_token(token: str):
    return decode_token(token)


# @users_router.post("/create-admin")
# async def register_admin(user: UserCreate, db: Session = Depends(dependencies.get_db)):
#     existing_user = db.query(User).filter(User.email == user.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail='User already registred.')
#
#     data = user.model_dump()
#     data.update({"role": "ADMIN"})
#     token = jwt.encode(data, secret_key, algorithm='HS256')
#
#     db_user = User(**data)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#
#     return token
