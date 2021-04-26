from fastapi import APIRouter, Depends

from apps.user import router as user_router
from apps.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(user_router, prefix='/user', tags=["用户"])

api_router.include_router(auth_router, prefix='/auth', tags=["权限管理"])

__all__ = ["api_router"]
