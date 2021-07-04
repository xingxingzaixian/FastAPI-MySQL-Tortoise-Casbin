# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 基础模型
"""
from typing import Any

from tortoise import fields
from tortoise.models import Model
from pydantic import BaseModel, Field


class TimestampMixin:
    created_at = fields.DatetimeField(
        null=True, auto_now_add=True, description="创建时间")
    modified_at = fields.DatetimeField(
        null=True, auto_now=True, description="更新时间")


class AbstractBaseModel(Model):
    id = fields.IntField(pk=True)
    is_delete = fields.IntField(
        null=False, default=0, description="逻辑删除:0=未删除,1=删除")

    class Meta:
        abstract = True
