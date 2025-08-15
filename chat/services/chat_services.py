from fastapi import WebSocketDisconnect

from chat.db.message.model import Message
from users.db.models import User
from common.utils import decode_token



active_connections = {}


async def connect_user(user_id, websocket):
    await websocket.accept()
    active_connections[user_id] = websocket


async def send_personal_message(message: dict, user_id: int):
    if user_id in active_connections:
        await active_connections[user_id].send_json(message)


async def chat_websocket(websocket, receiver_id, db, token):
    user_data = decode_token(token)
    current_user = db.query(User).filter(User.email == user_data["email"]).first()
    await connect_user(current_user.id, websocket)
    try:
        while True:
            data = await websocket.receive_text()

            msg = Message(
                sender_id=current_user.id,
                receiver_id=receiver_id,
                content=data
            )
            db.add(msg)
            db.commit()
            db.refresh(msg)

            await send_personal_message({
                "content": data,
                "sender": current_user.username,
                "sender_id": current_user.id,
                "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }, receiver_id)

    except WebSocketDisconnect:
        active_connections.pop(current_user.id, None)


async def get_chat(user_id, page, page_size, db, token):
    user_data = decode_token(token)
    current_user = db.query(User).filter(User.email == user_data["email"]).first()
    offset = (page - 1) * page_size
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at).offset(offset).limit(page_size).all()
    return messages

