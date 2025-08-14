from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from users.schemas.schemas import UserBase
from products.schemas.product.schemas import ProductCreateSchema
from users.services.users_services import register
from common.utils import decode_token
from dependencies import get_db



users_router = APIRouter(prefix="/users")

@users_router.post("/register")
async def register_endpoint(user: UserBase, db: Session = Depends(get_db)):
    return await register(user, db)


@users_router.get("/check-info")
async def check_info_from_token(token: str = Header()):
    return decode_token(token)
