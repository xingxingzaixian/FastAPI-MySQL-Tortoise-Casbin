# -*- coding: utf-8 -*-
""" 
@author: xingxingzaixian
@create: 2021/4/23
@description: 重载casbin适配器，使用tortoise-orm作为表处理
"""
import asyncio

from casbin import persist
from tortoise import fields, models


class CasbinRule(models.Model):
    ptype = fields.CharField(max_length=255)
    v0 = fields.CharField(max_length=255)
    v1 = fields.CharField(max_length=255)
    v2 = fields.CharField(max_length=255)
    v3 = fields.CharField(max_length=255)
    v4 = fields.CharField(max_length=255)
    v5 = fields.CharField(max_length=255)

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ', '.join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.pk, str(self))

    class Meta:
        table = 'casbin_rule'


class Filter:
    ptype = []
    v0 = []
    v1 = []
    v2 = []
    v3 = []
    v4 = []
    v5 = []


class Adapter(persist.Adapter):
    """the interface for Casbin adapters."""

    def __init__(self, db_class=None, filtered=False):
        if db_class is None:
            db_class = CasbinRule
        self._db_class = db_class
        self._filtered = filtered

    def load_policy(self, model):
        """
        数据库的操作是由异步库 Tortoise 执行的，因此在同步函数中需要通过此方式运行
        :param model:
        :return:
        """
        # 获取当前正在运行的时间循环，如果没有就创建一个
        loop = asyncio.get_event_loop()

        # 将一个coroutine协程对象提交给指定的事件循环
        asyncio.run_coroutine_threadsafe(self._load_policy(model), loop)

    async def _load_policy(self, model):
        """loads all policy rules from the storage."""
        lines = await self._db_class.all()
        for line in lines:
            persist.load_policy_line(str(line), model)

    def is_filtered(self):
        return self._filtered

    def load_filtered_policy(self, model, filter) -> None:
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._load_filtered_policy(model, filter), loop)

    async def _load_filtered_policy(self, model, filter) -> None:
        """loads all policy rules from the storage."""
        filters = await self.filter_query(self._db_class, filter)
        filters = await filters.all()

        for line in filters:
            persist.load_policy_line(str(line), model)
        self._filtered = True

    async def filter_query(self, querydb, filter):
        ret = []
        if len(filter.ptype) > 0:
            ret = await querydb.filter(ptype__in=filter.ptype).order_by(CasbinRule.id)
            return ret
        if len(filter.v0) > 0:
            ret = await querydb.filter(v0__in=filter.v0).order_by(CasbinRule.id)
            return ret
        if len(filter.v1) > 0:
            ret = await querydb.filter(v1__in=filter.v1).order_by(CasbinRule.id)
            return ret
        if len(filter.v2) > 0:
            ret = await querydb.filter(v2__in=filter.v2).order_by(CasbinRule.id)
            return ret
        if len(filter.v3) > 0:
            ret = await querydb.filter(v3__in=filter.v3).order_by(CasbinRule.id)
            return ret
        if len(filter.v4) > 0:
            ret = await querydb.filter(v4__in=filter.v4).order_by(CasbinRule.id)
            return ret
        if len(filter.v5) > 0:
            ret = await querydb.filter(v5__in=filter.v5).order_by(CasbinRule.id)
            return ret

    async def _save_policy_line(self, ptype, rule):
        line = self._db_class(ptype=ptype)
        for i, v in enumerate(rule):
            setattr(line, "v{}".format(i), v)
        await line.save()

    def save_policy(self, model):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._save_policy(model), loop)

    async def _save_policy(self, model):
        """saves all policy rules to the storage."""
        await self._db_class.all().delete()
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    await self._save_policy_line(ptype, rule)
        return True

    def add_policy(self, sec, ptype, rule):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._add_policy(sec, ptype, rule), loop)

    async def _add_policy(self, sec, ptype, rule):
        """adds a policy rule to the storage."""
        await self._save_policy_line(ptype, rule)

    def remove_policy(self, sec, ptype, rule):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._remove_policy(sec, ptype, rule), loop)

    async def _remove_policy(self, sec, ptype, rule):
        """removes a policy rule from the storage."""
        query = await self._db_class.filter(self._db_class.ptype == ptype)
        for i, v in enumerate(rule):
            query = await query.filter(getattr(self._db_class, "v{}".format(i)) == v)
        r = await query.delete()

        return True if r > 0 else False

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self._remove_filtered_policy(sec, ptype, field_index, *field_values), loop)

    async def _remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """removes policy rules that match the filter from the storage.
        This is part of the Auto-Save feature.
        """
        query = await self._db_class.filter(self._db_class.ptype == ptype)
        if not (0 <= field_index <= 5):
            return False
        if not (1 <= field_index + len(field_values) <= 6):
            return False
        for i, v in enumerate(field_values):
            query = await query.filter(getattr(self._db_class, "v{}".format(field_index + i)) == v)
        r = await query.delete()

        return True if r > 0 else False
