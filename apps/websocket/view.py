# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/7/4
@description: 
"""
from typing import Dict

from fastapi import APIRouter, WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.types import Receive, Scope, Send

from .manage import WebScoketManage
from utils.ws_tools import get_websocket_query_params

router = APIRouter()
manage = WebScoketManage()


class BaseWebSocket(WebSocketEndpoint):
    encoding = 'json'

    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        super().__init__(scope, receive, send)
        self.group_name = 'publish'
        self.params = None

    async def on_connect(self, websocket: WebSocket) -> None:
        await manage.connect(self.group_name, websocket, self.params)
        await websocket.accept()

    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        await manage.disconnect(self.group_name, websocket)


@router.websocket_route('/info')
class InfoWebSocket(BaseWebSocket):
    async def on_connect(self, websocket: WebSocket) -> None:
        # key = self.scope['path_params'].get('key')
        # self.group_name = f'custom_group_{key}'
        await super().on_connect(websocket)

    async def on_receive(self, websocket: WebSocket, data: Dict) -> None:
        await manage.broadcast(self.group_name, data, websocket)
