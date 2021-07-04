# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/7/4
@description: 
"""

from typing import Dict

from fastapi import WebSocket
from pydantic.utils import import_string

from utils.ws_tools import get_websocket_uid
from utils.logger import logger


class WebSocketItem:
    def __init__(self, websocket: WebSocket, params=None) -> None:
        self.websocket = websocket
        self.params = params


class WebScoketManage:
    def __init__(self) -> None:
        self.active_connections: Dict[str, Dict[str, WebSocketItem]] = {}

    async def connect(self, group_name: str, websocket: WebSocket, params=None):
        websocket_uid = get_websocket_uid(websocket)
        if group_name in self.active_connections:
            self.active_connections[group_name][websocket_uid] = WebSocketItem(
                websocket, params)
        else:
            self.active_connections[group_name] = {
                websocket_uid: WebSocketItem(websocket, params)}

        logger.info(f'有新的客户端连接， websocket： {websocket}, 客户端数量：{len(self.active_connections[group_name])}')

    async def disconnect(self, group_name: str, websocket: WebSocket):
        websocket_uid = get_websocket_uid(websocket)
        if group_name in self.active_connections:
            self.active_connections[group_name].pop(websocket_uid)

        logger.info(f'关闭客户端连接，websocket：{websocket}，客户端数量：{len(self.active_connections[group_name])}')
        await websocket.close()

    async def broadcast(self, group_name: str, message: dict, websocket: WebSocket, callback=None):
        """
        广播消息到指定客户端
        """
        if group_name not in self.active_connections:
            return

        for _, item in self.active_connections[group_name].items():
            # 只发送给当前组的其他人，过滤掉自己
            if item.websocket == websocket:
                continue

            if callback:
                result = callback(item.params, message)
            else:
                result = message

            await item.websocket.send_json(result)
