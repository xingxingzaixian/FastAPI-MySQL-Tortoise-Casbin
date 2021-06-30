from typing import Type

from tortoise.models import Model


class Router:
    def db_for_read(self, model: Type[Model]):
        return "default"

    def db_for_write(self, model: Type[Model]):
        return "default"
