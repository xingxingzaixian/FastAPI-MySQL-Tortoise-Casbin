import casbin
import casbin_tortoise_adapter
from fastapi import Request
from typing import Any

from core import settings
from utils.custom_exc import AuthenticationError
from utils.utils import Singleton


class TortoiseCasbin(metaclass=Singleton):
    def __init__(self, model: str) -> None:
        print('*'*20, '初始化 casbin')
        adapter = casbin_tortoise_adapter.TortoiseAdapter()
        self.enforce = casbin.Enforcer(str(model), adapter)

    async def has_permission(self, user: str, model: str, act: str) -> bool:
        """
        判断是否拥有权限
        """
        return self.enforce.enforce(user, model, act)

    async def add_permission_for_role(self, role: str, model: str, act: str):
        """
        添加角色权限
        """
        return await self.enforce.add_policy(role, model, act)

    async def remove_permission_for_role(self, role: str, model: str, act: str):
        return await self.enforce.remove_policy(role, model, act)

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.enforce, attr)


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
        model, act = self.policy.split(',')
        e = await get_casbin()

        # 超级用户拥有所有权限
        if request.state.user.is_super:
            return

        if not await e.has_permission(request.state.user.username, model, act):
            raise AuthenticationError(err_desc=f'Permission denied: [{self.policy}]')


async def check_authority(policy):
    """
    进行权限认证
    :param policy: 字符串，以 user,model,act拼接而成，例如"user,auth,add"
    :return:
    """
    user, model, act = policy.split(',')
    e = await get_casbin()
    if not await e.has_permission(user, model, act):
        raise AuthenticationError(err_desc=f'Permission denied: [{policy}]')


async def get_casbin() -> TortoiseCasbin:
    """
    获取 casbin 权限认证对象，初始化时要加载一次权限模型信息
    :return:
    """
    tor_casbin = TortoiseCasbin(settings.CASBIN_MODEL_PATH)
    if not hasattr(tor_casbin, 'load'):
        setattr(tor_casbin, 'load', True)
        await tor_casbin.load_policy()
    return tor_casbin
