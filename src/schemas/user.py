from pydantic import BaseModel, EmailStr


class Register_User_Schema(BaseModel):
    username: str
    email: EmailStr
    password: str


class Login_User_Schema(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
