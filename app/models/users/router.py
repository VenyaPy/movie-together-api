from fastapi import APIRouter, HTTPException, status, Response, Depends, UploadFile, File
from app.models.users.model import Users
from app.models.users.schemas import SUserReg, SUserAuth
from app.models.users.dao import UserDAO
from app.models.users.security import get_password_hash, authenticate_user, create_access_token
from app.models.users.dependencies import get_current_user

import uuid
import aiofiles


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


@router_auth.post("/login", status_code=201)
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("token_access", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout", status_code=201)
async def logout_user(response: Response):
    response.delete_cookie("token_access")


@router_user.get("/me")
async def get_user_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router_user.post("/upload-photo/")
async def upload_user_photo(
    current_user: Users = Depends(get_current_user),
    file: UploadFile = File(...)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    file_extension = file.filename.split(".")[-1]
    if file_extension not in ("jpg", "jpeg", "png"):
        raise HTTPException(status_code=400, detail="Invalid file extension")

    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"app/models/users/images/{file_name}"

    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    await file.seek(0)

    # Обновляем путь к файлу в профиле пользователя, используя ID, а не username
    update_result = await UserDAO.update(id=current_user.id, image=file_path)
    if update_result == 0:
        raise HTTPException(status_code=404, detail="Ошибка обновления данных пользователя")

    return {"file_name": file_name, "file_path": file_path}


