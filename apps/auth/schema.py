# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from typing import Any

from pydantic import BaseModel, Field


# 创建API
class AuthCreate(BaseModel):
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


class AuthOut(BaseModel):
    auth: str = Field(..., description='权限字符串')
