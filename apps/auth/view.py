# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from typing import List

from fastapi import APIRouter, Request, Depends, HTTPException

from auth.auth_casbin import get_casbin, Authority, check_authority
from .schema import AuthCreate, AuthOut
from apps.user.crud import get_user_by_name
from utils.response_code import HttpStatus, ResultResponse

router = APIRouter()


@router.post(
    "/add",
    summary="添加访问权限",
    description="添加访问权限",
    response_model=ResultResponse[AuthOut],
    dependencies=[Depends(Authority('auth,add'))]
)
async def add_authority(
        authority_info: AuthCreate
):
    user = await get_user_by_name(authority_info.role)
    if not user:
        return ResultResponse[str](code=HttpStatus.HTTP_419_USER_EXCEPT, message='添加权限的用户不存在，请检查用户名')

    e = await get_casbin()
    res = e.add_policy(authority_info.role, authority_info.model, authority_info.act)
    if res:
        return ResultResponse[AuthOut](message='权限添加成功', data={'auth': f'{authority_info.role},{authority_info.model},{authority_info.act}'})
    else:
        return ResultResponse[str](message='添加失败，权限已存在')


@router.post(
    "/del",
    summary="删除访问权限",
    description='删除用户权限',
    response_model=ResultResponse[str],
    dependencies=[Depends(Authority('auth,remove'))]
)
async def del_authority(
        authority_info: AuthCreate
):
    e = await get_casbin()
    res = e.remove_policy(authority_info.role, authority_info.model, authority_info.act)
    if res:
        return ResultResponse[str](message='权限已删除')
    else:
        return ResultResponse[str](message='删除失败，权限不存在')


@router.get(
    '/list',
    summary='获取所有权限列表',
    description='获取所有权限列表',
    response_model=ResultResponse[List[List]]
)
async def get_authority_list():
    e = await get_casbin()
    result = e.get_policy()
    return ResultResponse[List[List]](data=result)


@router.get(
    '/permission',
    summary='获取当前用户权限列表',
    description='获取当前用户权限列表',
    response_model=ResultResponse[List[List]]
)
async def get_authority(request: Request):
    e = await get_casbin()
    result = e.get_filtered_policy(0, request.state.user.username)
    return ResultResponse[List[List]](data=result)
