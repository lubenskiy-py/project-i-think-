from fastapi import FastAPI
from users.routers.routers import users_router

app = FastAPI()

app.include_router(users_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

"""
post http://127.0.0.1:8000/register

{
    "username":"username",
    "email":"test@gmal.com",
    "password":"1234"
}
"""


"""
from fastapi import APIRouter, FastAPI

app = FastAPI()
internal_router = APIRouter()
users_router = APIRouter()

@users_router.get("/users/")
def read_users():
    return [{"name": "Rick"}, {"name": "Morty"}]

internal_router.include_router(users_router)
app.include_router(internal_router)
"""