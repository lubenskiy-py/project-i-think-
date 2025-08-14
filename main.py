from fastapi import FastAPI
import ngrok

from load_env import ngrok_token
from users.routers.user import users_router
from users.routers.admin import admins_router
from products.routers.routers import products_router
from chat.routers.routers import chat_router



listener = ngrok.forward(8000, authtoken=ngrok_token)
print(listener.url())

app = FastAPI()

app.include_router(users_router)
app.include_router(admins_router)
app.include_router(products_router)
app.include_router(chat_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
