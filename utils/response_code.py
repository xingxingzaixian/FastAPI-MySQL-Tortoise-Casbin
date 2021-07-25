from typing import Generic, TypeVar, Optional
from pydantic import Field
from pydantic.generics import GenericModel

Data = TypeVar('Data')


class ResultResponse(GenericModel, Generic[Data]):
    """
    自定义返回模型，使用 generic-models 定义自定义模型
    https://pydantic-docs.helpmanual.io/usage/models/#generic-models
    所有返回数据都用如下格式，方便前端统一处理
    {
        code: 200,
        message: '请求成功',
        data: None
    }
    """
    code: int = Field(default=200, description='返回码')
    message: str = Field(default='请求成功', description='消息内容')
    result: Optional[Data]


class HttpStatus:
    # 请求正常
    HTTP_200_OK = 200

    # 用户登录异常
    HTTP_418_AUTH_EXCEPT = 418

    # 用户不存在
    HTTP_419_USER_EXCEPT = 419

    # Token 过期
    HTTP_420_TOKEN_EXCEPT = 420

    # 内部参数校验失败
    HTTP_421_INNER_PARAM_EXCEPT = 421

    # 角色不存在
    HTTP_422_ROLE_NOT_EXIST = 422

    # 请求参数格式错误
    HTTP_422_QUERY_PARAM_EXCEPT = 422

    # Authentication 权限异常
    HTTP_425_AUTHENTICATION_EXCEPT = 425

    # 服务端错误
    HTTP_500_INTERNAL_SERVER_ERROR = 500

    # 角色不存在
    HTTP_600_ROLE_NOT_EXIST = 600

    # 角色不存在
    HTTP_601_ROLE_EXIST = 601
