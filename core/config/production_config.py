import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = True

    # 项目文档
    TITLE: str = "FastAPI+MySQL项目生成"
    DESCRIPTION: str = "更多FastAPI知识，请关注我的个人网站 https://www.charmcode.cn/"

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 生成token的加密算法
    ALGORITHM: str = "HS256"

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = 'aeq)s(*&(&)()WEQasd8**&^9asda_asdasd*&*&^+_sda'

    # 项目根路径
    BASE_PATH: str = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))

    # RBAC 权限认证配置路径
    CASBIN_MODEL_PATH = os.path.join(BASE_PATH, 'core/config/rbac_model.conf')

    # 超级管理员
    SUPER_USER: str = 'super'

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
                    'apps.'
                ]
            }
        }
    }


settings = Settings()
