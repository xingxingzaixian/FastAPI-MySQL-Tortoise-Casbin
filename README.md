# FastAPI+MySQL+Tortoise-orm项目模板
## 简介
使用FastAPI + MySql + Tortoise-orm 作为主要数据库操作,项目结构参考:
- [CoderCharm
/
fastapi-mysql-generator](https://github.com/CoderCharm/fastapi-mysql-generator)
- [FastAPI-demo](https://github.com/FutureSenzhong/FastAPI-demo)

## 功能
- JWT token 认证。
- 使用 Tortoise-orm models(MySql).
- 基于 casbin 的权限验证
- loguru 日志模块使用

## 项目文件组织

## 权限控制
- 登录、注册及路由中含有openapi的接口不进行登录和权限认证
```python
async def jwt_authentication(
        request: Request,
        x_token: str = Header(
            None,
            title='登录Token',
            description='登录、注册及开放API不需要此参数'
        )
):
    """
            除了开放API、登录、注册以外，其他均需要认证
            :param request:
            :return:
            """
    if 'openapi' in request.url.path.lower() or \
            'login' in request.url.path.lower() or \
            'register' in request.url.path.lower():
        return None
    ....
```
- 全局登录认证（除以上接口外，其余接口均进行登录认证）

登录认证成功后, request.state 会添加一个 user 属性，在所有地方可以通过 request.state.user 获取当前用户信息 
```python
app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        dependencies=[Depends(jwt_authentication)]
    )
```
全局进行 Depends(jwt_authentication) 依赖注入
- 接口权限认证

首先通过 auth/add 和 auth/del 接口进行权限配置
```python
@router.get(
    "/info",
    summary="获取当前用户信息",
    name="获取当前用户信息",
    response_model=schema.UserOut,
    response_model_exclude_unset=True,
    dependencies=[Depends(Authority('user,check'))]
)
```
在接口上添加 Depends(Authority('user,check')) 依赖注入来判断权限
- 操作权限认证

在接口中进行特殊权限认证，只要使用check_authority函数判断即可，如果无权限会抛出异常
```python
await check_authority(f'{request.state.user.username},auth,add')
```

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
                'apps.'
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