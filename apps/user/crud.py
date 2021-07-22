# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/26
@description: 所有对数据库的操作
"""
from typing import List, Union, Any

from tortoise.exceptions import DoesNotExist

from . import schema
from .model import TblUser, RoleCreate, TblRole
from utils.utils import get_password_hash

from apps import user


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


async def create_user(user_data: schema.UserCreate) -> TblUser:
    user = TblUser(**user_data.dict(exclude={'confirm'}))
    user.password = get_password_hash(user_data.password)
    await user.save()
    return user


async def create_role(role_data: RoleCreate) -> TblRole:
    role = TblRole(**role_data.dict())
    await role.save()
    return role


async def get_role_by_name(role_name: str) -> Union[TblRole, Any]:
    try:
        role = TblRole.get(name=role_name)
    except DoesNotExist as exec:
        return None
    return role


async def get_user_list() -> List[TblUser]:
    return await TblUser.all()