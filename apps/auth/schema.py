# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from typing import Any

from pydantic import BaseModel, Field


# 角色权限
class RolePerm(BaseModel):
    role: str = Field(..., description='角色')
    model: str = Field(..., description='模块')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'role': 'guest',
                'model': 'auth',
                'act': 'add'
            }
        }


# 用户权限配置
class UserPerm(BaseModel):
    user: str = Field(..., description='用户名')
    model: str = Field(..., description='模块')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'user': 'zhangsan',
                'model': 'user',
                'act': 'add'
            }
        }


# 用户角色配置
class UserRole(BaseModel):
    user: str = Field(..., description='用户名')
    role: str = Field(..., description='角色')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'user': 'zhangsan',
                'role': 'guest'
            }
        }