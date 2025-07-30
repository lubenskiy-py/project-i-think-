from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from init_db import get_db
from users.db.models import User
from users.schemas.schemas import UserCreate, UserLogin

import uuid

users_router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_current_user(credentials: HTTPAuthorizationCredentials, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.token == credentials.credentials).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid authorization credentials.')

    return user


@users_router.post('/register')
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(user.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='User already registred.')

    hashed_password = pwd_context.hash(user.password)
    token = str(uuid.uuid4())
    db_user = User(
        username=user.username,
        email=str(user.email),
        hashed_password=hashed_password,
        token=token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {'message': 'User created.', 'token': token}


@users_router.post('/login')
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail='Invalid email.')

    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid password.')

    return {'message': 'Login successful.', 'token': db_user.token}
