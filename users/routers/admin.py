from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from users.schemas.schemas import UserBase
from dependencies import get_db
from products.schemas.category.schemas import CategoryCreateSchema
from products.schemas.product.schemas import TagCreateSchema
from users.services.admins_services import (
    create_category,
    register_admin,
    create_tag,
    create_super_admin,
    delete_tag,
    delete_category,
)



admins_router = APIRouter(prefix="/admins")

@admins_router.post("/create-super-admin")
async def create_super_admin_endpoint(user: UserBase, db: Session = Depends(get_db)):
    return await create_super_admin(user, db)


@admins_router.post("/register-admin")
async def register_admin_endpoint(user: UserBase, token: str = Header(), db: Session = Depends(get_db)):
    return await register_admin(user, token, db)


@admins_router.post("/create-category")
async def create_category_endpoint(category: CategoryCreateSchema, token: str = Header(), db: Session = Depends(get_db)):
    return await create_category(category, token, db)


@admins_router.delete("/delete-category")
async def delete_category_endpoint(category_name: str, token: str = Header(), db: Session = Depends(get_db)):
    return await delete_category(category_name, token, db)


@admins_router.post("/create-tag")
async def create_tag_endpoint(tag: TagCreateSchema, token: str = Header(), db: Session = Depends(get_db)):
    return await create_tag(tag, token, db)


@admins_router.delete("/delete-tag/{tag_name}")
async def delete_tag_endpoint(tag_name: str, token: str = Header(), db: Session = Depends(get_db)):
    return await delete_tag(tag_name, token, db)
