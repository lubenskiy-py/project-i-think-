from fastapi import FastAPI
from users.routers.user import users_router
from users.routers.admin import admins_router
from products.routers.routers import products_router

app = FastAPI()

app.include_router(users_router)
app.include_router(admins_router)
app.include_router(products_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
