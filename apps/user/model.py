"""
数据库表模型定义
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from core.model import AbstractBaseModel, TimestampMixin


class TblRole(TimestampMixin, AbstractBaseModel):
    name = fields.CharField(max_length=32, unique=True, description='角色名')
    description = fields.CharField(max_length=256, description='角色描述')

    class Meta:
        table = 'tbl_role'
        table_description = '角色表'
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "is_delete"]


class TblUser(TimestampMixin, AbstractBaseModel):
    username = fields.CharField(max_length=64, unique=True)
    nickname = fields.CharField(max_length=128, null=True)
    mobile = fields.CharField(max_length=15, null=True)
    email = fields.CharField(max_length=64, unique=True, null=True)
    password = fields.CharField(max_length=128, null=False)
    avatar = fields.CharField(max_length=256, null=True)

    class Meta:
        table = "tbl_user"
        table_description = "用户表信息"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "password", 'is_delete']


UserBase = pydantic_model_creator(TblUser, name="UserBase")
UserOut = pydantic_model_creator(
    TblUser,
    name='UserOut',
    include=['username', 'nickname', 'mobile', 'email'])

RoleCreate = pydantic_model_creator(TblRole, name='RoleCreate')
RoleOut = pydantic_model_creator(TblRole, name='RoleOut')