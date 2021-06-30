import json
from typing import List

from fastapi import WebSocket

from utils.logger import logger


class DataParse:
    @classmethod
    def parse_params_all(cls, params: List, message: str):
        """
        根据连接的参数和设备数据
        :param params:
        :param message:
        :return:
        """
        data = message
        result = {
            "params": params,
            "data": data
        }
        return result

    @classmethod
    def parse_params_101(cls, params: List, message: str):
        """
        根据连接的参数和设备数据
        :param params:
        :param message:
        :return:
        """
        data = message
        result = {
            "params": params,
            "data": data
        }

        return result

    @classmethod
    def parse_params_201(cls, params: List, message: str):
        """
        根据连接的参数和设备数据
        :param params:
        :param message:
        :return:
        """
        data = message
        result = {
            "params": params,
            "data": data
        }

        return result

    @classmethod
    def parse_params_402(cls, params: List, message: str):
        """
        根据连接的参数和设备数据
        :param params:
        :param message:
        :return:
        """
        data = message
        result = {
            "params": params,
            "data": data
        }

        return result


def get_websocket_uid(websocket: WebSocket):
    """
    获取 WebSocket 的唯一标记
    :param websocket:
    :return:
    """
    socket_str = str(websocket)[1:-1]
    socket_list = socket_str.split(' ')
    socket_only = socket_list[3]
    return socket_only


def get_websocket_query_params(query_string):
    """
    获取 websocket 的 Query 参数
    :param query_string:
    :return:
    """
    query_params = {}
    try:
        for line in query_string.split('&'):
            item = line.split('=')
            query_params[item[0]] = item[1]
    except Exception as e:
        logger.error(f'请求参数格式错误: {query_string}')

    return query_params


def get_device_message_group(message):
    """
    根据消息内容，获取消息应该发送的分组
    :param message: {'path': 10133111313131, 'data': 10}
    :return:
    """
    path = str(message.get('path'))
    return f'device/{path[:3]}', path[:3]
