import traceback

from fastapi import FastAPI, Request, Depends, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, ValidationError
from tortoise.contrib.fastapi import register_tortoise

from .router import api_router
from .middleware import register_hook
from utils import custom_exc
from utils.logger import logger
from core.config import settings


def create_app() -> FastAPI:
    """
    生成FatAPI对象
    :return:
    """
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL
    )

    # 跨域设置
    register_cors(app)

    # 注册路由
    register_router(app)

    # 注册捕获全局异常
    register_exception(app)

    # 请求拦截
    register_hook(app)

    # 取消挂载在 request对象上面的操作，感觉特别麻烦，直接使用全局的
    register_init(app)
    return app


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(api_router)


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception(app: FastAPI) -> None:
    """
    全局异常捕获
    注意 别手误多敲一个s
    exception_handler
    exception_handlers
    两者有区别
        如果只捕获一个异常 启动会报错
        @exception_handlers(UserNotFound)
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    # 自定义异常 捕获
    @app.exception_handler(custom_exc.TokenExpired)
    async def user_not_found_exception_handler(request: Request, exc: custom_exc.TokenExpired):
        """
        token过期
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(status_code=settings.HTTP_418_EXCEPT, content={'message': 'Token 已过期，请重新登录', 'desc': exc.err_desc})

    @app.exception_handler(custom_exc.TokenAuthError)
    async def user_token_exception_handler(request: Request, exc: custom_exc.TokenAuthError):
        """
        用户token异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return JSONResponse(status_code=settings.HTTP_418_EXCEPT, content={'message': '用户认证异常，请重新登录', 'desc': exc.err_desc})

    @app.exception_handler(custom_exc.AuthenticationError)
    async def user_not_found_exception_handler(request: Request, exc: custom_exc.AuthenticationError):
        """
        用户权限不足
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户权限不足 \nURL:{request.method}{request.url}")
        return JSONResponse(status_code=settings.HTTP_418_EXCEPT, content={'message': '权限不足', 'desc': exc.err_desc})

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(status_code=settings.HTTP_418_EXCEPT, content={'message': '内部参数校验失败', 'desc': exc.errors()})

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(status_code=settings.HTTP_418_EXCEPT, content={'message': '请求参数校验异常', 'desc': exc.errors()})

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'message': '服务器异常'})


def register_init(app: FastAPI) -> None:
    """
    初始化连接
    :param app:
    :return:
    """

    @app.on_event("startup")
    async def init_connect():
        # 连接数据库
        register_tortoise(
            app,
            config=settings.DATABASE_CONFIG,
            # modules=settings.DATABASE_CONFIG.get("apps").get("models"),
            generate_schemas=True,  # True 表示连接数据库的时候同步创建表
            add_exception_handlers=True,
        )
        logger.info("start server and register_tortoise")
        # 连接redis
        # redis_client.init_redis_connect()

        # 初始化 apscheduler
        # schedule.init_scheduler()

    @app.on_event('shutdown')
    async def shutdown_connect():
        """
        关闭
        :return:
        """
        # schedule.shutdown()
        logger.info('stop server')
