from fastapi import APIRouter, WebSocket, Depends, HTTPException, status

from uuid import uuid4

from app.models.users.model import Users
from app.models.users.dependencies import get_current_user
from app.models.session.sessiondao import SessionDAO
from datetime import datetime


room_router = APIRouter(
    tags=["Комнаты для просмотра"],
)


rooms = {}


@room_router.post("/create_room/{movie_id}")
async def create_room(movie_url: str, current_user: Users = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не авторизованы"
        )

    room_id = str(uuid4())

    session_data = {
        "room_id": room_id,
        "user_id": current_user.username,
        "movie_id": movie_url,
        "time": datetime.now()
    }

    try:
        new_session = await SessionDAO.add(**session_data)
        if not new_session:
            raise HTTPException(status_code=500, detail="Не удалось создать сессию")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {e}")

    return {"room_id": room_id}


@room_router.websocket("/ws/{room_id}")
async def websocket_end(websocket: WebSocket):
    await websocket.accept()

