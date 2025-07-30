from fastapi import APIRouter

products_router = APIRouter()

@products_router.post("/product")
async def create_product():
    ...