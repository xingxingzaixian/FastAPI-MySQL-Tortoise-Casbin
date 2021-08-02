# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/26
@description: 所有对数据库的操作
"""
from typing import List, Union, Any

from tortoise.exceptions import DoesNotExist

from . import schema
from auth.auth_casbin import get_casbin
from .model import TblUser, RoleCreate, TblRole
from utils.utils import get_password_hash


async def get_user_by_name(username: str) -> Union[TblUser, Any]:
    """
    :param username:
    :return:
    """
    try:
        user: TblUser = await TblUser.get(username=username)
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
    """
    获取角色信息
    """
    try:
        role: TblRole = await TblRole.get(name=role_name)
    except DoesNotExist as exec:
        return None
    return role


async def delete_role_by_name(role_name: str) -> bool:
    """
    删除角色信息，同时删除 casbin 中角色信息
    """
    role: TblRole = await get_role_by_name(role_name)
    if role:
        role.is_delete = 1
        await role.save()

        # 删除 casbin 的角色权限
        e = await get_casbin()
        e.delete_role(role_name)

        return True
    return False


async def has_role(role_name: str) -> bool:
    """
    判断是否包含角色信息
    """
    role: TblRole = await get_role_by_name(role_name)
    if role and not role.is_delete:
        return True
    return False


async def get_user_list() -> List[TblUser]:
    return await TblUser.all()