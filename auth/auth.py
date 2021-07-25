from datetime import datetime, timedelta

from jose import jwt
from fastapi import Request, Header
from starlette.authentication import AuthenticationError
from pydantic import ValidationError

from core import settings
from utils import custom_exc
from apps.user.crud import get_user_by_name


def create_access_token(
        subject: str,
        expires_delta: timedelta = None
) -> str:
    """
    生成token
    :param subject:需要存储到token的数据(注意token里面的数据，属于公开的)
    :param authority_id: 权限id(用于权限管理)
    :param expires_delta:
    :return:
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "username": subject}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def jwt_authentication(
        request: Request,
        access_token: str = Header(
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
    for url, op in settings.NO_VERIFY_URL.items():
        if op == 'eq' and url == request.url.path.lower():
            return None
        elif op == 'in' and url in request.url.path.lower():
            return None

    if access_token is None:
        raise custom_exc.TokenAuthError()

    try:
        playload = jwt.decode(
            access_token,
            settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise custom_exc.TokenExpired()
    except (jwt.JWTError, ValidationError, AttributeError):
        raise custom_exc.TokenAuthError()

    username = playload.get('username')
    user = await get_user_by_name(username=username)
    if not user:
        raise AuthenticationError("认证失败")

    """在 Request 对象中设置用户对象，这样在其他地方就能通过 request.state.user 获取到当前用户了"""
    request.state.user = user
