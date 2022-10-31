# Применимость: Паттерн встречается в Python не так уж часто, так как для его применения нужна цепь объектов, например, связанный список.
# Признаки применения паттерна: Цепочку обязанностей можно определить по спискам обработчиков или проверок, через которые пропускаются запросы. Особенно если порядок следования обработчиков важен.

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler(ABC):
    """
    Интерфейс Обработчика объявляет метод построения цепочки обработчиков. Он
    также объявляет метод для выполнения запроса.
    """
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler: ...
    @abstractmethod
    def handle(self, request) -> str | None: ...


class AbstractHandler(Handler):
    """
    Поведение цепочки по умолчанию может быть реализовано внутри базового класса
    обработчика.
    """
    _next_handler: Handler = None
    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler
    @abstractmethod
    def handle(self, request: Any) -> str | None:
        if self._next_handler:
            return self._next_handler.handle(request)


"""
Все Конкретные Обработчики либо обрабатывают запрос, либо передают его
следующему обработчику в цепочке.
"""
class HandlerOne(AbstractHandler):
    def handle(self, request: Any) -> str | None:
        if request == "One":
            return "First Handler"
        else:
            return super().handle(request)
class HandlerTwo(AbstractHandler):
    def handle(self, request: Any) -> str | None:
        if request == "Two":
            return "Second Handler"
        else:
            return super().handle(request)
class HandlerThree(AbstractHandler):
    def handle(self, request: Any) -> str | None:
        if request == "Three":
            return "Third Handler"
        else:
            return super().handle(request)


def client_code(handler: Handler):
    print()
    for num in ['1', 'One', 'ten', 'Three']:
        print(f"client: {num}", end='')
        if result := handler.handle(num):
            print("\t", result)
        else:
            print("\t Fail")


if __name__ == "__main__":
    one = HandlerOne()
    two = HandlerTwo()
    three = HandlerThree()
    one.set_next(two).set_next(three)

    client_code(one)
    client_code(two)
    client_code(three)
