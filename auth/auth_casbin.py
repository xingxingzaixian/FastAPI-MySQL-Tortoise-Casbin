import casbin
from fastapi import Request

from core.config import settings
from auth import casbin_tortoise_adapter
from utils.custom_exc import AuthenticationError


def get_casbin() -> casbin.Enforcer:
    """
    获取 casbin 权限认证对象
    :return:
    """
    adapter = casbin_tortoise_adapter.Adapter()
    e = casbin.Enforcer(settings.CASBIN_MODEL_PATH, adapter)
    return e


class Authority:
    def __init__(self, policy: str):
        """
        :param policy:
        """
        self.policy = policy

    def __call__(self, request: Request):
        """
        超级管理员不需要进行权限认证
        :param request:
        :return:
        """
        sub = request.state.user.username
        if settings.SUPER_USER and sub == settings.SUPER_USER:
            return

        obj, act = self.policy.split(',')
        e = get_casbin()
        if not e.enforce(sub, obj, act):
            raise AuthenticationError(err_desc=f'Permission denied: [{self.policy}]')