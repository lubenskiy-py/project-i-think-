from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from products.schemas.product.schemas import ProductCreateSchema, ProductUpdateSchema
from dependencies import get_db
from products.services.products_services import (
    create_product,
    delete_product,
    update_product,
    show_product,
    list_products,
    list_categories,
    list_products_by_category,
    list_tags,
)



products_router = APIRouter(prefix="/products")


@products_router.post("/create-product")
async def create_product_endpoint(product: ProductCreateSchema, token: str = Header(), db: Session = Depends(get_db)):
    return await create_product(product, token, db)


@products_router.delete("/delete-product/{product_id}")
async def delete_product_endpoint(product_id: int, token: str = Header(), db: Session = Depends(get_db)):
    return await delete_product(product_id, token, db)


@products_router.put("/update-product/{product_id}")
async def update_product_endpoint(product_id: int, product: ProductUpdateSchema, token: str = Header(), db: Session = Depends(get_db)):
    return await update_product(product_id, product, token, db)


@products_router.get("/")
async def get_products_endpoint(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        min_price: float = Query(None, ge=0),
        max_price: float = Query(None, ge=0),
        search: str = Query(None, min_length=1),
        tags: list[str] = Query(None),
        sort_by: str = Query(None, regex="^(price|title)$"),
        sort_order: str = Query("asc", regex="^(asc|desc)$"),
        token: str = Header(),
        db: Session = Depends(get_db)
):
    return await list_products(
        page, page_size, token, db,
        min_price=min_price,
        max_price=max_price,
        search=search,
        tags=tags,
        sort_by=sort_by,
        sort_order=sort_order
    )


@products_router.get("/categories")
async def list_categories_endpoint(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=20),
        token: str = Header(),
        db: Session = Depends(get_db)
):
    return await list_categories(page, page_size, token, db)


@products_router.get("/categories/{category_name}")
async def get_products_in_category_endpoint(
        category_name: str,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=20),
        token: str = Header(),
        db: Session = Depends(get_db)
):
    return await list_products_by_category(category_name, page, page_size, token, db)


@products_router.get("/tags")
async def list_tags_endpoint(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=20),
        token: str = Header(),
        db: Session = Depends(get_db)
):
    return await list_tags(page, page_size, token, db)


@products_router.get("/{product_id}")
async def show_product_endpoint(product_id: int, token: str = Header(), db: Session = Depends(get_db)):
    return await show_product(product_id, token, db)
