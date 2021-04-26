"""
请求参数模型
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, AnyHttpUrl


class Token(BaseModel):
    access_token: str
    token_type: str


# Shared properties
class UserBase(BaseModel):
    username: str
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: int = None


# 创建账号需要验证的条件
class UserCreate(BaseModel):
    username: str
    nickname: Optional[str] = None
    email: EmailStr
    mobile: Optional[str] = None
    password: str
    avatar: Optional[AnyHttpUrl] = None


# 返回用户信息
class UserOut(UserBase):
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
