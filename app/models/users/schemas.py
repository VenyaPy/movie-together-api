from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    username: str
    password: str


class SUserReg(SUserAuth):
    email: EmailStr
