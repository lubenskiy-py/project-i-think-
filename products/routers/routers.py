from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from products.schemas.product.schemas import ProductCreateSchema
from dependencies import get_db
from common.utils import check_role, decode_token
from products.db.product.models import Product, Tag
from products.db.category.models import Category


products_router = APIRouter(prefix="/products")

@products_router.post("/create-product")
async def create_product(product: ProductCreateSchema, token: str = Header(), db: Session = Depends(get_db)):
    if check_role(token) != "USER":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    tag_objects = []
    for tag_name in product.tags:
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag doesn't exist")
        tag_objects.append(tag)

    new_product = product.model_dump()
    new_product["tags"] = tag_objects
    if not new_product["owner_email"]:
        new_product["owner_email"] = decode_token(token)["email"]
    category = db.query(Category).filter(Category.name == new_product["category"]).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category doesn't exist")
    new_product.pop("category")
    new_product["category_id"] = category

    db_product = Product(**new_product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {"message": "Product has been added.", "product": db_product}
