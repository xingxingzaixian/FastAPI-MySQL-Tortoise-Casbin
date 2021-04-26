# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/26
@description: 所有对数据库的操作
"""
from typing import Union, Any

from tortoise.exceptions import DoesNotExist

from . import schema
from .model import TblUser, UserModel
from utils.utils import get_password_hash


async def get_user_by_name(username: str) -> Union[TblUser, Any]:
    """
    :param username:
    :return:
    """
    try:
        user = await TblUser.get(username=username)
    except DoesNotExist as exc:
        return None
    return user


async def create_user(user_data: schema.UserCreate) -> UserModel:
    user = TblUser(**user_data.dict())
    user.password_hash = get_password_hash(user_data.password)
    await user.save()
    return user
