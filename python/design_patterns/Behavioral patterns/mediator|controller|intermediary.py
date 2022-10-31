# Применимость: Пожалуй, самое популярное применение Посредника в Python-коде — это связь нескольких компонентов GUI одной программы.

from __future__ import annotations
from abc import ABC


class Mediator(ABC):
    """
    Интерфейс Посредника предоставляет метод, используемый компонентами для
    уведомления посредника о различных событиях. Посредник может реагировать на
    эти события и передавать исполнение другим компонентам.
    """
    def notify(self, sender: object, event: str): ...


class ConcreteMediator(Mediator):
    def __init__(self, component_1: Component1, component_2: Component2) -> None:
        self._component_1 = component_1
        self._component_1.mediator = self
        self._component_2 = component_2
        self._component_2.mediator = self
    def notify(self, sender: object, event: str):
        if event == "A1":
            print("Mediator: D event")
            self._component_2.do_d()
        elif event == "C2":
            print("Mediator: C event")
            self._component_1.do_a()
            self._component_1.do_b()
            self._component_2.do_d()


class BaseComponent:
    """
    Базовый Компонент обеспечивает базовую функциональность хранения экземпляра
    посредника внутри объектов компонентов.
    """
    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator
    @property
    def mediator(self) -> Mediator:
        return self._mediator
    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator
"""
Конкретные Компоненты реализуют различную функциональность. Они не зависят от
других компонентов. Они также не зависят от каких-либо конкретных классов
посредников.
"""
class Component1(BaseComponent):
    def do_a(self):
        print("Component1: A")
        self.mediator.notify(self, "A1")
    def do_b(self):
        print("Component1: B")
        self.mediator.notify(self, "B1")
class Component2(BaseComponent):
    def do_c(self):
        print("Component2: C")
        self.mediator.notify(self, "C2")
    def do_d(self):
        print("Component2: D")
        self.mediator.notify(self, "D2")


if __name__ == "__main__":
    c1 = Component1()
    c2 = Component2()
    mediator = ConcreteMediator(c1, c2)
    
    c1.do_a()
    print("-"*60)
    c1.do_b()
    print("-"*60)
    c2.do_c()
    print("-"*60)
    c2.do_d()