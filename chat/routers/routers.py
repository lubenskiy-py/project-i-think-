from fastapi import APIRouter, WebSocket, Header, Depends, Query
from sqlalchemy.orm import Session

from chat.services.chat_services import chat_websocket, get_chat
from dependencies import get_db



chat_router = APIRouter(prefix="/chat")


@chat_router.websocket("/{receiver_id}")
async def chat_websocket_endpoint(websocket: WebSocket, receiver_id: int, token: str = Header(), db: Session = Depends(get_db)):
    return await chat_websocket(websocket, receiver_id, db, token)


@chat_router.get("/{receiver_id}")
async def chat_endpoint(
        receiver_id: int,
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100),
        token: str = Header(),
        db: Session = Depends(get_db)):
    return await get_chat(receiver_id, page, page_size, db, token)
