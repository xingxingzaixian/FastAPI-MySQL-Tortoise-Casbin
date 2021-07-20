from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from apps.user import router as user_router
from apps.auth import router as auth_router
from apps.websocket import router as websocket_router
from core.config import settings

api_router = APIRouter(prefix='/api')


@api_router.get('/', include_in_schema=False)
async def index():
    return RedirectResponse(url=settings.DOCS_URL)


api_router.include_router(user_router, prefix='/user', tags=["用户"])
api_router.include_router(auth_router, prefix='/auth', tags=["权限管理"])
api_router.include_router(websocket_router, prefix='/ws', tags=['WebSocket 消息'])

__all__ = ["api_router"]
