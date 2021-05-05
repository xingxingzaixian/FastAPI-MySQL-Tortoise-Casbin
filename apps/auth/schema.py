# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from pydantic import BaseModel, Field


# 创建API
class AuthCreate(BaseModel):
    sub: str = Field(..., description='用户名')
    obj: str = Field(..., description='权限字符串')
    act: str = Field(..., description='权限行为')

    class Config:
        """
        schema_extra中设置参数的例子，在API文档中可以看到
        """
        schema_extra = {
            'example': {
                'sub': 'guest',
                'obj': 'auth',
                'act': 'add'
            }
        }
