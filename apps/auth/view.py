# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
import asyncio

from fastapi import APIRouter, Request, Depends

from auth.auth_casbin import get_casbin, Authority
from .schema import AuthCreate

router = APIRouter()


@router.post(
    "/add/auth",
    summary="添加访问权限",
    description="添加访问权限",
    dependencies=[Depends(Authority('auth,add'))]
)
async def add_authority(
        request: Request,
        authority_info: AuthCreate
):
    e = get_casbin()
    await asyncio.sleep(0.1)
    res = e.add_policy(request.state.user.username, authority_info.obj, authority_info.act)
    if res:
        return {'message': '权限添加成功', 'auth': f'{request.state.user.username},{authority_info.obj},{authority_info.act}'}
    else:
        return {'message': '添加失败，权限已存在'}


@router.post(
    "/del/auth",
    summary="删除访问权限",
    description='删除用户权限',
    dependencies=[Depends(Authority('auth,remove'))]
)
async def del_authority(
        request: Request,
        authority_info: AuthCreate
):
    e = get_casbin()

    # 异步执行时，为了保证某些程序执行的顺序，这里加上主动协程切换
    await asyncio.sleep(0.1)
    res = e.remove_policy(request.state.user.username, authority_info.obj, authority_info.act)
    if res:
        return {'message': '权限已删除'}
    else:
        return {'message': '删除失败，权限不存在'}
