from fastapi import APIRouter, HTTPException, status, Response
from app.models.users.schemas import SUserReg, SUserAuth
from app.models.users.dao import UserDAO
from app.models.users.security import get_password_hash, authenticate_user, create_access_token

router_auth = APIRouter(
    prefix="/auth",
    tags=["Регистрация и аутентификация"],
)


router_user = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserReg):
    have_user = await UserDAO.find_one_or_none(username=user_data.username)
    if have_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Аккаунт уже зарегистрирован"
        )
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(username=user_data.username,
                                 email=user_data.email,
                                 hashed_password=hashed_password)
    if not new_user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Не получилось создать пользователя"
        )


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("token_access", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("token_access")