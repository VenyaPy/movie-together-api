from fastapi import APIRouter


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


router_user = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


