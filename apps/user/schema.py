"""
请求参数模型
"""
from typing import Optional

from pydantic import BaseModel, EmailStr, AnyHttpUrl, Field


# Shared properties
class UserBase(BaseModel):
    username: str = Field(..., description='用户名')
    nickname: str = Field(None, description='用户昵称')
    email: EmailStr = Field(None, description='邮箱')
    mobile: str = Field(None, description='手机号')


class Token(BaseModel):
    access_token: str = Field(..., description='Token值')
    token_type: str = Field(..., description='Token类型')


# 创建账号需要验证的条件
class UserCreate(UserBase):
    password: str = Field(..., description='密码')
    avatar: AnyHttpUrl = Field(None, description='头像')
    role: str = Field(default='guest', description='角色，默认Guest')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'username': 'guest',
                'nickname': '访客',
                'email': 'guest@example.com',
                'mobile': '10086',
                'password': '123456',
                'avatar': 'https://img2.woyaogexing.com/2021/05/03/dfcfaaffa8ed4e1a819eba8c10b856d4!400x400.jpeg',
                'role': 'guest'
            }
        }

# 返回用户信息
class UserOut(UserBase):
    pass


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str = Field(None, description='修改的密码')
