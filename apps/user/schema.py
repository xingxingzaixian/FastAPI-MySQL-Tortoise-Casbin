"""
请求参数模型
"""
from pydantic import BaseModel, Field, validator

from .model import UserBase


class Token(BaseModel):
    access_token: str = Field(..., description='Token值')
    token_type: str = Field(..., description='Token类型')


# 创建账号需要验证的条件
class UserCreate(UserBase):
    confirm: str = Field(..., description='确认密码')

    @validator('confirm')
    def validate_confirm(cls, value, values, config, field):
        """
        验证密码是否一致
        """
        if value != values.get('password'):
            raise ValueError('passwords do not match')
        return value

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
                'confirm': '123456',
                'avatar': 'https://img2.woyaogexing.com/2021/05/03/dfcfaaffa8ed4e1a819eba8c10b856d4!400x400.jpeg'
            }
        }
