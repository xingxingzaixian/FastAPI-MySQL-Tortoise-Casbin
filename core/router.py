from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from apps.websocket import router as websocket_router
from core.config import settings

api_router = APIRouter()


@api_router.get('/', include_in_schema=False)
async def index():
    return RedirectResponse(url=settings.DOCS_URL)


api_router.include_router(websocket_router, prefix='/ws', tags=["WebSocket管理"])

__all__ = ["api_router"]
