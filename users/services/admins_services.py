from fastapi import HTTPException, status
from jose import jwt

from common.utils import is_admin
from products.db.category.models import Category
from products.db.product.models import Tag
from users.schemas.schemas import CreateAdmin
from load_env import secret_key
from users.db.models import User



async def register_admin(user, token, db):
    is_admin(token)

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registred.')

    data = CreateAdmin(**user.model_dump())
    token = jwt.encode(data.model_dump(), secret_key, algorithm='HS256')

    db_user = User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return token


async def create_super_admin(user, db):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registred.')

    data = CreateAdmin(**user.model_dump())
    token = jwt.encode(data.model_dump(), secret_key, algorithm='HS256')

    db_user = User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return token


async def create_category(category, token, db):
    is_admin(token)

    existing_category = db.query(Category).filter(Category.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already exists.')

    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return {"message": "Category has been added.", "category": db_category}


async def delete_category(category_name, token, db):
    is_admin(token)

    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category doesn't exist")

    db.delete(category)
    db.commit()

    return {"message": "Category has been deleted."}


async def create_tag(tag, token, db):
    is_admin(token)

    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Tag already exists.')

    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return {"message": "Tag has been added.", "tag": db_tag}


async def delete_tag(tag_name, token, db):
    is_admin(token)

    tag = db.query(Tag).filter(Tag.name == tag_name).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag doesn't exist")

    db.delete(tag)
    db.commit()

    return {"message": "Tag has been deleted."}

