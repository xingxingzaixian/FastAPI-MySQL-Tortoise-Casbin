# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/7/4
@description: 
"""

from typing import List

from fastapi import WebSocket

from utils.logger import logger


def get_websocket_uid(websocket: WebSocket):
    """
    获取 websocket 的唯一标记
    """
    socket_str = str(websocket)[1:-1]
    socket_list = socket_str.split(' ')
    socket_only = socket_list[3]
    return socket_only


def get_websocket_query_params(query_string: str):
    """
    获取 websocket 的 Query 参数
    """
    query_params = {}
    try:
        for line in query_string.split('&'):
            item = line.split('=')
            query_params[item[0]] = item[1]
    except Exception as e:
        logger.error(f'请求参数格式错误：{query_string}')

    return query_params
