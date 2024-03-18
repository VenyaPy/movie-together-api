from fastapi import APIRouter
from app.models.users.schemas import SUserAuth


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router_user = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    pass