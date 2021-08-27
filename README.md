# 更新记录
### 2021-08-27
1. 删除主分支中 WebSocket 功能，因为 WebSocket 并发部署很麻烦，如果有人需要 WebSocket 功能，请下载 websocket 分支

### 2021-08-08
1. 使用 asynccabin 库操作 casbin 权限处理模块
注意这个库的源文件与casbin库的源文件目录相同，因此在安装的时候会出现覆盖的情况，如果安装完后有异常，可以使用`pip uninstall asynccasbin`卸载这个库，然后重新安装即可
2. 修复权限处理模块异常
3. 增加了 OpenAPI 的统一认证功能，为了适配此功能，登录模块的返回值未采用统一的返回格式

![](https://tva1.sinaimg.cn/large/008i3skNly1gt9nowgcofj314c0mrjtt.jpg)

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
- [fastapi-mysql-generator](https://github.com/CoderCharm/fastapi-mysql-generator)
- [FastAPI-demo](https://github.com/FutureSenzhong/FastAPI-demo)

## 功能
- JWT token 认证。
- 使用 Tortoise-orm models(MySQL).
- 基于 casbin 的权限验证
- loguru 日志模块使用
- 增加 WebSocket 功能

## 项目文件组织

## 权限控制
- 登录、注册及路由中含有openapi的接口不进行登录和权限认证
```python
# 重载了 FastAPI.OAuth2 模块进行登录认证，此模块可以在 API 文档界面进行统一登录认证
# 为了适配这个功能登录接口的返回数据未采用统一格式，使用的时候需要注意
class OAuth2CustomJwt(OAuth2):
    ......
    async def __call__(self, request: Request) -> Optional[str]:
        """
        除了开放API、登录、注册、WebSocket接口外，其他接口均需要登录验证
        """
        for url, op in settings.NO_VERIFY_URL.items():
            if op == 'eq' and url == request.url.path.lower():
                return None
            elif op == 'in' and url in request.url.path.lower():
                return None

        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None

        try:
            playload = jwt.decode(
                param,
                settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise custom_exc.TokenExpired()
        except (jwt.JWTError, ValidationError, AttributeError):
            raise custom_exc.TokenAuthError()

        username = playload.get('username')
        user = await get_user_by_name(username=username)
        if not user:
            raise AuthenticationError("认证失败")

        """在 Request 对象中设置用户对象，这样在其他地方就能通过 request.state.user 获取到当前用户了"""
        request.state.user = user
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
        dependencies=[Depends(OAuth2CustomJwt(tokenUrl="/user/login"))]
    )
```
全局进行 Depends(OAuth2CustomJwt(tokenUrl="/user/login")) 依赖注入

- 接口权限认证

首先通过以下接口进行权限配置

![](https://tva1.sinaimg.cn/large/008i3skNly1gt9npof3euj31480brq4v.jpg)

在接口上添加 Depends(Authority('user,check')) 依赖注入来判断权限
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

- 操作权限认证

在接口中进行特殊权限认证，只要使用check_authority函数判断即可，如果无权限会抛出异常
```python
await check_authority(f'{request.state.user.username},auth,add')
```

## 配置
在 settings.py 中是进行项目配置，config/.env 文件中通过环境变量进行发布环境配置

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

设置用户的 is_super = 1，就表示超级管理员，超级管理员拥有所有权限，可以跳过权限认证
```python
class Authority:
    ......
    async def __call__(self, request: Request):
        """
        超级管理员不需要进行权限认证
        :param request:
        :return:
        """
        model, act = self.policy.split(',')
        e = await get_casbin()

        # 超级用户拥有所有权限
        if request.state.user.is_super:
            return

        if not await e.has_permission(request.state.user.username, model, act):
            raise AuthenticationError(err_desc=f'Permission denied: [{self.policy}]')
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
pipenv run dev
```

