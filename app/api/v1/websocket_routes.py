from fastapi import APIRouter, WebSocket, Query, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.websockets.manager import manager
from app.services import user_service
from app.db.session import get_db
from app.utils.jwt import decode_access_token

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)

        if payload is None:
            await websocket.close(code=1008)
            return

        user_id = payload.get("sub")

        if user_id is None:
            await websocket.close(code=1008)
            return

        user = user_service.get_current_user(db, int(user_id))

        if not user:
            await websocket.close(code=1008)
            return

    except Exception:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, user.role_id)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)