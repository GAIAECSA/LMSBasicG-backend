from fastapi import APIRouter, WebSocket, Query
from app.websockets.manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    role_id: int = Query(...)
):
    await manager.connect(websocket, role_id)

    try:
        while True:
            await websocket.receive_text()
    except:
        manager.disconnect(websocket)