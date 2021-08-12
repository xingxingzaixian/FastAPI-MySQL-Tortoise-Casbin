from datetime import datetime, timedelta
from typing import Optional, Dict

from jose import jwt
from fastapi import Request, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.authentication import AuthenticationError
from pydantic import ValidationError
from fastapi.security.utils import get_authorization_scheme_param

from core import settings
from utils import custom_exc
from apps.user.crud import get_user_by_name


class OAuth2CustomJwt(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        for url, op in settings.NO_VERIFY_URL.items():
            if op == 'eq' and url == request.url.path.lower():
                return None
            elif op == 'in' and url in request.url.path.lower():
                return None

        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        try:
            playload = jwt.decode(
                param,
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
