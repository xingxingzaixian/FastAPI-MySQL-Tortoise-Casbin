from .settings import Settings


class DevSettings(Settings):
    # 开发模式配置
    DEBUG: bool = True

    # 超级管理员
    SUPER_USER: str = 'super'

    # 异常请求返回码
    HTTP_418_EXCEPT = 418

    DATABASE_CONNECTS = {
        'default': 'mysql://root:xingxing123456@101.34.19.90:13456/testdb'
    }


settings = DevSettings()
