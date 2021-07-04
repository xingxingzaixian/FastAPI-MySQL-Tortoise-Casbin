"""
日志文件配置 参考链接
https://github.com/Delgan/loguru
"""

import os
import time
from loguru import logger

from core.config import settings


# 定位到log日志文件
log_path = os.path.join(settings.BASE_PATH, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_warning = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_warning.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置 文件区分不同级别的日志
logger.add(log_path_info, rotation="50 MB", encoding='utf-8', enqueue=True, level='INFO')
logger.add(log_path_warning, rotation="50 MB", encoding='utf-8', enqueue=True, level='WARNING')
logger.add(log_path_error, rotation="50 MB", encoding='utf-8', enqueue=True, level='ERROR')


__all__ = ["logger"]