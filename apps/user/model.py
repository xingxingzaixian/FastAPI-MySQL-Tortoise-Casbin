"""
数据库表模型定义
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from core.model import AbstractBaseModel, TimestampMixin


class TblUser(TimestampMixin, AbstractBaseModel):
    username = fields.CharField(max_length=64, unique=True)
    nickname = fields.CharField(max_length=128, null=True)
    mobile = fields.CharField(max_length=15, null=True)
    email = fields.CharField(max_length=64, unique=True, null=True)
    password_hash = fields.CharField(max_length=128, null=False)
    avatar = fields.CharField(max_length=256, null=True)
    is_active = fields.BooleanField(null=True, default=False, description="邮箱是否激活 0=未激活 1=激活")

    class Meta:
        table = "tbl_user"
        table_description = "user info table"
        ordering = ["-created_at", "id"]

    class PydanticMeta:
        exclude = ["created_at", "modified_at", "id", "password_hash"]


UserModel = pydantic_model_creator(TblUser, name="TblUser")
