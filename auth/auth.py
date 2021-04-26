from jose import jwt
from fastapi import Request, Header
from starlette.authentication import AuthenticationError
from pydantic import ValidationError

from core.config import settings
from utils import custom_exc
from apps.user.crud import get_user_by_name


async def jwt_authentication(
        request: Request,
        x_token: str = Header(
            None,
            title='登录Token',
            description='登录、注册及开放API不需要此参数'
        )
):
    """
            除了开放API、登录、注册以外，其他均需要认证
            :param request:
            :return:
            """
    if 'openapi' in request.url.path.lower() or \
            'login' in request.url.path.lower() or \
            'register' in request.url.path.lower():
        return None

    if x_token is None:
        raise custom_exc.TokenAuthError()

    try:
        playload = jwt.decode(
            x_token,
            settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise custom_exc.TokenExpired()
    except (jwt.JWTError, ValidationError, AttributeError):
        raise custom_exc.TokenAuthError()

    username = playload.get('sub')
    user = await get_user_by_name(username=username)
    if not user:
        raise AuthenticationError("认证失败")

    """在 Request 对象中设置用户对象，这样在其他地方就能通过 request.state.user 获取到当前用户了"""
    request.state.user = user
