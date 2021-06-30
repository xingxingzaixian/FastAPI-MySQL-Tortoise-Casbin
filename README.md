# FastAPI+MySQL+Tortoise-orm项目模板
## 简介
使用FastAPI + MySql + Tortoise-orm 作为主要数据库操作,项目结构参考:
- [CoderCharm
/
fastapi-mysql-generator](https://github.com/CoderCharm/fastapi-mysql-generator)
- [FastAPI-demo](https://github.com/FutureSenzhong/FastAPI-demo)

## 功能
PS: 此分支去掉了用户管理和权限认证，主要是为快速开发通用功能使用
- 使用 Tortoise-orm models(MySql).
- loguru 日志模块使用
- 支持 WebSocket 功能


## 项目文件组织


## 配置
配置文件：core/config/development_config.py 和 production_config.py

- 修改 API 文档默认地址

为了通过权限认证，将 API 文档地址修改为包含 openapi 的 URL
```python
# 文档地址 默认为docs
DOCS_URL: str = "/openapi/docs"
# 文档关联请求数据接口
OPENAPI_URL: str = "/openapi/openapi.json"
# redoc 文档
REDOC_URL: Optional[str] = "/openapi/redoc"
```

- 超级管理员

设置用户角色为 super 的用户为超级管理员
```python
SUPER_USER: str = 'super'
```

### 配置数据库
```python
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
    }
}
```

## 运行
```shell script
# 进入项目目录
pipenv install

# 进入虚拟环境
pipenv shell

# 运行服务器
python run.py
```