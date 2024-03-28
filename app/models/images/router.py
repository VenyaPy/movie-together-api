from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File

from app.models.users.model import Users
from app.models.users.dao import UserDAO
from app.models.users.dependencies import get_current_user
from app.tasks.tasks import process_pic

import uuid
import aiofiles


image_router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)


@image_router.post("/upload-photo/")
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
    file_path = f"app/images/save/{file_name}"

    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    await file.seek(0)

    update_result = await UserDAO.update(id=current_user.id, image=file_name)
    if update_result == 0:
        raise HTTPException(status_code=404, detail="Ошибка обновления данных пользователя")

    process_pic.delay(path=file_path)