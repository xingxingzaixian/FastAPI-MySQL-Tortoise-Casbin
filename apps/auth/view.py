# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 
"""
from fastapi import APIRouter, Request

from auth.auth_casbin import get_casbin
from utils import response_code
from .schema import AuthCreate

router = APIRouter()


@router.post("/add/auth", summary="添加访问权限", name="添加访问权限", description="添加访问权限")
async def add_authority(
        request: Request,
        authority_info: AuthCreate
):
    e = get_casbin()
    res = e.add_policy(request.state.user.username, authority_info.obj, authority_info.act)
    if res:
        return response_code.resp_200()
    else:
        return response_code.resp_4001(message="添加失败，权限已存在")


@router.post("/del/auth", summary="删除访问权限", name='删除权限', description='删除用户权限')
async def del_authority(
        request: Request,
        authority_info: AuthCreate
):
    e = get_casbin()
    res = e.remove_policy(request.state.user.username, authority_info.obj, authority_info.act)
    if res:
        return response_code.resp_200()
    else:
        return response_code.resp_4001(message="删除失败，权限不存在")
