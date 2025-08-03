import os
import base64

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from dotenv import load_dotenv

from users.db.models import User
from users.schemas.schemas import UserCreate
import dependencies



admins_router = APIRouter()

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

@admins_router.post("/register-admin")
async def register_admin(user: UserCreate, token: str = Header(), db: Session = Depends(dependencies.get_db)):
    check_token = dependencies.decode_token(token)

    if check_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token(and you)")

    if check_token["role"] != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registred.')

    data = user.model_dump()
    data.update({"role": "ADMIN"})
    new_admin_token = jwt.encode(data, secret_key, algorithm='HS256')

    db_user = User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return new_admin_token



@admins_router.post("/create-admin")
async def register_admin(user: UserCreate, db: Session = Depends(dependencies.get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='User already registred.')

    data = user.model_dump()
    data.update({"role": "ADMIN"})
    token = jwt.encode(data, secret_key, algorithm='HS256')

    db_user = User(**data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return token
