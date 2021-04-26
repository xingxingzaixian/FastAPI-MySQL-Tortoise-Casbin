# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from pydantic import BaseModel


# 创建API
class AuthCreate(BaseModel):
    obj: str
    act: str
