# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from typing import List

from fastapi import APIRouter, Request, Depends, HTTPException

from auth.auth_casbin import get_casbin, Authority, check_authority
from .schema import AuthCreate
from apps.user.crud import get_user_by_name
from core.config import settings

router = APIRouter()


@router.post(
    "/add",
    summary="添加访问权限",
    description="添加访问权限",
    dependencies=[Depends(Authority('auth,add'))]
)
async def add_authority(
        authority_info: AuthCreate
):
    user = await get_user_by_name(authority_info.sub)
    if not user:
        raise HTTPException(status_code=settings.HTTP_418_EXCEPT, detail='添加权限的用户不存在，请检查用户名')

    e = await get_casbin()
    res = e.add_policy(authority_info.sub, authority_info.obj, authority_info.act)
    if res:
        return {'message': '权限添加成功', 'auth': f'{authority_info.sub},{authority_info.obj},{authority_info.act}'}
    else:
        return {'message': '添加失败，权限已存在'}


@router.post(
    "/del",
    summary="删除访问权限",
    description='删除用户权限',
    dependencies=[Depends(Authority('auth,remove'))]
)
async def del_authority(
        authority_info: AuthCreate
):
    e = await get_casbin()
    res = e.remove_policy(authority_info.sub, authority_info.obj, authority_info.act)
    if res:
        return {'message': '权限已删除'}
    else:
        return {'message': '删除失败，权限不存在'}


@router.get(
    '/list',
    summary='获取所有权限列表',
    description='获取所有权限列表',
    response_model=List[List]
)
async def get_authority_list():
    e = await get_casbin()
    result = e.get_policy()
    return result


@router.get(
    '/permission',
    summary='获取权限列表',
    description='获取权限列表',
    response_model=List
)
async def get_authority(request: Request):
    e = await get_casbin()
    result = e.get_filtered_policy(0, request.state.user.username)
    return result
