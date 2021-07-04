import asyncio

import casbin
from fastapi import Request
from asgiref.sync import async_to_sync, sync_to_async

from core.config import settings
from auth import casbin_tortoise_adapter
from utils.custom_exc import AuthenticationError


async def get_casbin() -> casbin.Enforcer:
    """
    获取 casbin 权限认证对象
    :return:
    """
    adapter = casbin_tortoise_adapter.Adapter()
    e = casbin.Enforcer(settings.CASBIN_MODEL_PATH, adapter)

    # 加上sleep是为了主动切换协程
    await asyncio.sleep(0.01)
    return e


class Authority:
    def __init__(self, policy: str):
        """
        :param policy:
        """
        self.policy = policy

    async def __call__(self, request: Request):
        """
        超级管理员不需要进行权限认证
        :param request:
        :return:
        """

        # 超级用户拥有所有权限
        role = request.state.user.role
        if settings.SUPER_USER and role == settings.SUPER_USER:
            return

        model, act = self.policy.split(',')
        e = await get_casbin()
        if not e.enforce(role, model, act):
            raise AuthenticationError(err_desc=f'Permission denied: [{self.policy}]')


async def check_authority(policy):
    """
    进行权限认证
    :param policy: 字符串，以 role,model,act拼接而成，例如"admin,auth,add"
    :return:
    """
    role, model, act = policy.split(',')
    e = await get_casbin()
    if not e.enforce(role, model, act):
        raise AuthenticationError(err_desc=f'Permission denied: [{policy}]')
