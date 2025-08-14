from fastapi import APIRouter, WebSocket

from chat.services.chat_services import chat
from chat.schemas.message.schemas import Message


chat_router = APIRouter(prefix="/chat")

@chat_router.websocket("/")
async def chat_endpoint(websocket: WebSocket):
    return await chat(websocket)
