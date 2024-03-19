from fastapi import Depends, Request, HTTPException, status, File, UploadFile
from jose import ExpiredSignatureError, JWTError, jwt


from app.models.users.security import UserDAO


def get_token(request: Request):
    token = request.cookies.get("token_access")
    if not token:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Вы не авторизованы")
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, "venpopugorjaln204kd0", algorithms="HS256")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_423_LOCKED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Токен не найден 3")
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Токен не найден 4")
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user_id:
        raise HTTPException(status_code=status.HTTP_423_LOCKED, detail="Токен не найден 5")

    return user

