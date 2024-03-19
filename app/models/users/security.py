from datetime import datetime, timedelta
from fastapi import HTTPException, status

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.models.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hash_pass) -> bool:
    return pwd_context.verify(plain_password, hash_pass)


def create_access_token(data: dict) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=180)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "venpopugorjaln204kd0", algorithm="HS256")
        return encoded_jwt
    except Exception as e:
        print(e)


async def authenticate_user(username: str, password: str):
    user = await UserDAO.find_one_or_none(username=username)
    if not (user and verify_password(password, user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль"
        )
    return user  # Возвращаем объект user в случае успешной аутентификации
