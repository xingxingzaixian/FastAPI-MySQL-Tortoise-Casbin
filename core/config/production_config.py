import os
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = True

    # 项目文档
    TITLE: str = "FastAPI+MySQL+Tortoise-orm项目生成"
    DESCRIPTION: str = "FastAPI 基于 Tortoise-orm 实现的大型项目框架"
    # 文档地址 默认为docs
    DOCS_URL: str = "/openapi/docs"
    # 文档关联请求数据接口
    OPENAPI_URL: str = "/openapi/openapi.json"
    # redoc 文档
    REDOC_URL: Optional[str] = "/openapi/redoc"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'aeq)s(*&(&)()WEQasd8**&^9asda_asdasd*&*&^+_sda'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

    # 超级管理员
    SUPER_USER: str = 'super'

    # 异常请求返回码
    HTTP_418_EXCEPT = 418

    # 数据库配置
    DATABASE_CONFIG: dict = {
        'connections': {
            # Dict format for connection
            'default': 'mysql://root:123456@127.0.0.1:3306/testdb'
        },
        'apps': {
            'models': {
                # 设置key值“default”的数据库连接
                'default_connection': 'default',
                'models': [
                ]
            }
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }

    # 不需要登录认证的 API
    NO_VERIFY_URL = {
        "/": "eq",                  # 根目录
        "openapi": "in",            # 开发 API
        "/user/login": "eq",        # 登录
        "/user/register": "eq",     # 注册
        "ws": "in"                  # ws 服务不需要登录
    }


settings = Settings()
