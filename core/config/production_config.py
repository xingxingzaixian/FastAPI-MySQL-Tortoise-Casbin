from .settings import Settings


class ProSettings(Settings):
    # 开发模式配置
    DEBUG: bool = False

    DATABASE_CONNECTS = {
        'default': 'mysql://root:xingxing123456@101.34.19.90:13456/testdb'
    }


settings = ProSettings()
