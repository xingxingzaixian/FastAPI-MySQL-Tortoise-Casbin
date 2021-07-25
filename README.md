# 更新记录
### 2021-07-25
1. 使用.env配置不同环境
2. 增加 Casbin 权限配置接口，具体文档：[Casbin使用](http://101.34.19.90:10086/project-2/doc-10/)

**注意：** WebSocket 不支持 Session 共享，所以如果在项目使用了 WebSocket 功能，则不能使用多进程或者分布式部署，WebSocket 的分布式部署需要借助其他的服务

### 2021-07-04
1. 增加 settings.py 配置文件，将通用配置写入，开发/发布环境各自单独配置
2. 修复权限验证 BUG
3. 增加 WebSocket 功能
4. 增加多数据库配置功能
5. 增加通用请求返回模板 ResultResponse

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
- 增加 WebSocket 功能

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
    for url, op in settings.NO_VERIFY_URL.items():
        if op == 'eq' and url == request.url.path.lower():
            return None
        elif op == 'in' and url in request.url.path.lower():
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
core/config/settings.py 中是通用配置，development_config.py 和 production_config.py 中配置开发环境和发布环境的配置项

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

### 多配置数据库
```python
# settings.py
DATABASE_CONNECTS = {
        'default': 'mysql://root:123456@127.0.0.1:3306/testdb'
    }

# 数据库配置
DATABASE_CONFIG: dict = {
    'connections': DATABASE_CONNECTS,
    'apps': {
        'models': {
            # 设置key值“default”的数据库连接
            'default_connection': 'default',
            'models': [
                'apps.user.model',
                'auth.casbin_tortoise_adapter'
            ]
        }
    }
}

# db_router.py
class Router:
    def db_for_read(self, model: Type[Model]):
        # 在模型定义的 Meta 中定义 default_connection 对应的数据库字符串即可
        if model._meta.default_connection:
            return model._meta.default_connection
        return "default"

    def db_for_write(self, model: Type[Model]):
        if model._meta.default_connection:
            return model._meta.default_connection
        return "default"
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

