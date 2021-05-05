"""
URL视图处理
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from . import crud, schema
from core.config import settings
from utils import logger
from utils.utils import verify_password
from auth.auth import create_access_token
from auth.auth_casbin import Authority

router = APIRouter()


@router.post("/login", summary="用户登录认证", response_model=schema.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    通过用户名和密码登录获取 token 值
    :param form_data:
    :return:
    """
    # 验证用户
    user = await crud.get_user_by_name(username=form_data.username)
    if not user:
        logger.info(f"用户名认证错误: username:{form_data.username} password:{form_data.password}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username or password error')

    # 验证密码
    if not verify_password(form_data.password, user.password_hash):
        logger.info(f"用户密码错误: username:{form_data.username} password:{form_data.password}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username or password error')

    # 登录成功后返回token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=user.username, expires_delta=access_token_expires)

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    '/register',
    summary='用户注册',
    description='注册新用户',
    response_model=schema.UserOut,
    response_model_exclude_unset=True
)
async def register(user: schema.UserCreate):
    user = await crud.create_user(user)
    return user


@router.get(
    "/info",
    summary="获取当前用户信息",
    name="获取当前用户信息",
    response_model=schema.UserOut,
    response_model_exclude_unset=True,
    dependencies=[Depends(Authority('user,check'))]
)
async def get_user_info(request: Request):
    return request.state.user
