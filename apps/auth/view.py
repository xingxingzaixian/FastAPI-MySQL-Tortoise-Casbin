# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from typing import List

from fastapi import APIRouter, Request, Depends

from auth.auth_casbin import get_casbin, Authority
from .schema import RolePerm, UserPerm, UserRole
from apps.user.crud import get_role_by_name, get_user_by_name
from utils.response_code import HttpStatus, ResultResponse

router = APIRouter()


@router.post("/add/role/perm",
             summary="添加角色权限",
             description="添加角色权限",
             response_model=ResultResponse[str],
             dependencies=[Depends(Authority('auth,add'))])
async def add_role_perm(perm_info: RolePerm):
    role = await get_role_by_name(perm_info.role)
    if not role:
        return ResultResponse[str](code=HttpStatus.HTTP_422_ROLE_NOT_EXIST,
                                   message='角色不存在')

    e = await get_casbin()
    res = await e.add_permission_for_role(perm_info.role, perm_info.model, perm_info.act)
    if res:
        return ResultResponse[str](message='添加角色权限成功')
    else:
        return ResultResponse[str](message='添加角色权限失败，权限已存在')


@router.post('/del/role/perm',
             summary='删除角色权限',
             description='删除角色权限',
             dependencies=[Depends(Authority('auth,del'))])
async def del_role_perm(perm_info: RolePerm):
    e = await get_casbin()
    res = await e.remove_permission_for_role(perm_info.role, perm_info.model, perm_info.act)
    if res:
        return ResultResponse[str](message='删除角色权限成功')
    return ResultResponse[str](message='角色权限不存在')


@router.post("/add/user/perm",
             summary="添加用户权限",
             description="添加用户权限",
             response_model=ResultResponse[str],
             dependencies=[Depends(Authority('auth,add'))])
async def add_user_perm(user_info: UserPerm):
    user = await get_user_by_name(user_info.user)
    if not user:
        return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT,
                                   message='添加权限的用户不存在，请检查用户名')

    e = await get_casbin()
    res = await e.add_permission_for_user(user_info.user, user_info.model,
                                    user_info.act)
    if res:
        return ResultResponse[str](message='添加用户权限添加成功')
    else:
        return ResultResponse[str](message='添加用户权限失败，权限已存在')


@router.post("/del/user/perm",
             summary="删除用户权限",
             description='删除用户权限',
             response_model=ResultResponse[str],
             dependencies=[Depends(Authority('auth,del'))])
async def del_user_perm(user_info: UserPerm):
    e = await get_casbin()
    res = await e.delete_permission_for_user(user_info.user, user_info.model,
                                       user_info.act)
    if res:
        return ResultResponse[str](message='删除用户权限成功')
    else:
        return ResultResponse[str](message='删除用户权限失败')


@router.post("/add/user/role",
             summary="添加用户角色",
             description="添加用户角色",
             response_model=ResultResponse[str],
             dependencies=[Depends(Authority('auth,add'))])
async def add_user_role(user_role: UserRole):
    user = await get_user_by_name(user_role.user)
    if not user:
        return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT,
                                   message='添加权限的用户不存在，请检查用户名')

    role = await get_role_by_name(user_role.role)
    if not role:
        return ResultResponse[str](code=HttpStatus.HTTP_422_ROLE_NOT_EXIST,
                                   message='角色不存在')

    e = await get_casbin()
    res = await e.add_role_for_user(user_role.user, user_role.role)
    if res:
        return ResultResponse[str](message='添加用户角色成功')
    else:
        return ResultResponse[str](message='添加用户角色失败')


@router.post('/del/user/role',
            summary='删除用户角色',
            description='删除用户角色',
            response_model=ResultResponse[str],
            dependencies=[Depends(Authority('auth,del'))]
)
async def del_user_role(user_role: UserRole):
    user = await get_user_by_name(user_role.user)
    if not user:
        return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT,
                                   message='用户不存在，请检查用户名')

    role = await get_role_by_name(user_role.role)
    if not role:
        return ResultResponse[str](code=HttpStatus.HTTP_422_ROLE_NOT_EXIST,
                                   message='角色不存在')

    e = await get_casbin()
    res = await e.delete_role_for_user(user_role.user, user_role.role)
    if res:
        return ResultResponse[str](message='删除用户角色成功')
    else:
        return ResultResponse[str](message='删除用户角色失败')


@router.get('/user/roles',
            summary='获取用户角色列表',
            description='获取用户角色列表',
            response_model=ResultResponse[List])
async def get_role_list(username: str):
    e = await get_casbin()
    result = await e.get_roles_for_user(username)
    return ResultResponse[List](result=result)


@router.post('/test',
            summary='权限测试接口',
            description='权限测试接口',
            response_model=ResultResponse[bool]
)
async def test_auth(test: UserPerm):
    e = await get_casbin()
    result = await e.has_permission(test.user, test.model, test.act)
    return ResultResponse[bool](result=result)