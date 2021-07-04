from .settings import Settings


class ProSettings(Settings):
    # 开发模式配置
    DEBUG: bool = False

    DATABASE_CONNECTS = {
        'default': 'mysql://root:123456@127.0.0.1:3306/testdb'
    }


settings = ProSettings()
