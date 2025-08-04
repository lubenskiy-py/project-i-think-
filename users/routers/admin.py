import os
import base64

from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from users.db.models import User
from users.schemas.schemas import UserCreate
from common.utils import decode_token, check_role
from dependencies import get_db
from load_env import secret_key
from products.schemas.category.schemas import CategoryCreateSchema
from products.schemas.product.schemas import TagCreateSchema
from products.db.category.models import Category
from products.db.product.models import Tag



admins_router = APIRouter(prefix="/admins")


# use it, if database don't have ADMIN.
@admins_router.post("/create-admin")
async def register_admin(user: UserCreate, db: Session = Depends(get_db)):
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


@admins_router.post("/register-admin")
async def register_admin(user: UserCreate, token: str = Header(), db: Session = Depends(get_db)):
    if check_role(token) != "ADMIN":
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


@admins_router.post("/create-category")
async def create_category(category: CategoryCreateSchema, token: str = Header(), db: Session = Depends(get_db)):
    if check_role(token) != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail='Category already exists.')

    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"message": "Category has been added.", "category": db_category}


@admins_router.post("/create-tag")
async def create_tag(tag: TagCreateSchema, token: str = Header(), db: Session = Depends(get_db)):
    if check_role(token) != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail='Tag already exists.')

    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return {"message": "Tag has been added.", "tag": db_tag}
