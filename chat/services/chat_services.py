from fastapi import HTTPException, status



async def chat(websocket):
    await websocket.accept()
    while True:
        try:
            message = await websocket.receive_text()
            print(message)
        except Exception as exc:
            print(f'Websocket error: {exc}')
            break
