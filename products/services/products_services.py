from fastapi import HTTPException, status
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import joinedload

from common.utils import decode_token, is_user
from products.db.category.models import Category
from products.db.product.models import Product, Tag
from users.db.models import User



async def create_product(product, token, db):
    is_user(token)

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
    new_product["category_id"] = category.id

    user = db.query(User).filter(User.email == new_product["owner_email"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist")
    new_product["user_id"] = user.id

    db_product = Product(**new_product)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {"message": "Product has been added.", "product": db_product}


async def delete_product(product_id, token, db):
    is_user(token)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product doesn't exist")

    user_email = decode_token(token)["email"]
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist")

    if product.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    db.delete(product)
    db.commit()

    return {"message": "Product has been deleted."}


async def update_product(product_id, new_product, token, db):
    is_user(token)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product doesn't exist")

    user_email = decode_token(token)["email"]
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exist")

    if product.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied.")

    data = new_product.model_dump(exclude_none=True)

    if data.get("tags") is not None:
        tag_objects = []
        for tag_name in data["tags"]:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                raise HTTPException(status_code=400, detail="Tag doesn't exist")
            tag_objects.append(tag)
        data["tags"] = tag_objects

    if data.get("category") is not None:
        category = db.query(Category).filter(Category.name == data["category"]).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category doesn't exist")
        data.pop("category")
        data["category_id"] = category.id

    for key, value in data.items():
        if value is not None:
            setattr(product, key, value)

    db.commit()

    return {"message": "Product has been updated."}


async def show_product(product_id, token, db):
    is_user(token)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product doesn't exist")

    return {"product": product}


async def list_products(
        page: int,
        page_size: int,
        token: str,
        db,
        category_name: str = None,
        min_price: float = None,
        max_price: float = None,
        search: str = None,
        tags: list[str] = None,
        sort_by: str = None,
        sort_order: str = "asc"
):
    is_user(token)

    offset = (page - 1) * page_size

    query = db.query(Product).options(joinedload(Product.tags))

    if category_name:
        query = query.join(Category).filter(Category.name.ilike(category_name))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Product.title.ilike(search_pattern)) |
            (Product.description.ilike(search_pattern))
        )

    if tags:
        query = (
            query.join(Product.tags)
            .filter(Tag.name.in_(tags))
            .group_by(Product.id)
            .having(func.count(func.distinct(Tag.id)) == len(tags))
        )

    if sort_by in ["price", "title"]:
        column = getattr(Product, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

    total = query.count()
    products = query.offset(offset).limit(page_size).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No products found")

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "products": products
    }


async def list_categories(page, page_size, token, db):
    is_user(token)

    offset = (page - 1) * page_size
    categories = db.query(Category).offset(offset).limit(page_size).all()

    if not categories:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page doesn't exist")

    return {
        "page": page,
        "page_size": page_size,
        "categories": categories
    }


async def list_products_by_category(category_name, page, page_size, token, db):
    is_user(token)

    offset = (page - 1) * page_size

    products_query = db.query(Product).join(Category).filter(Category.name.ilike(category_name))

    total = products_query.count()

    products = products_query.offset(offset).limit(page_size).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page doesn't exist")

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "products": products
    }


async def list_tags(page, page_size, token, db):
    is_user(token)

    offset = (page - 1) * page_size
    tags = db.query(Tag).offset(offset).limit(page_size).all()

    if not tags:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Page doesn't exist")

    return {
        "page": page,
        "page_size": page_size,
        "tags": tags
    }
