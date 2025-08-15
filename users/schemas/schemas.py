from pydantic import BaseModel, EmailStr, Field



class UserBase(BaseModel):
    username: str
    email: EmailStr


class CreateAdmin(UserBase):
    role: str = "ADMIN"


class CreateUser(UserBase):
    role: str = "USER"
