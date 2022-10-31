# Применимость: Посетитель нечасто встречается в Python-коде из-за своей сложности и нюансов реализазации.

from __future__ import annotations
from abc import ABC, abstractmethod


class Component(ABC):
    """
    Интерфейс Компонента объявляет метод accept, который в качестве аргумента
    может получать любой объект, реализующий интерфейс посетителя.
    """
    @abstractmethod
    def accept(self, visitor: Visitor): ...
class ConcreteComponentA(Component):
    """
    Каждый Конкретный Компонент должен реализовать метод accept таким образом,
    чтобы он вызывал метод посетителя, соответствующий классу компонента.
    """
    def accept(self, visitor: Visitor):
        """
        Обратите внимание, мы вызываем visitConcreteComponentA, что
        соответствует названию текущего класса. Таким образом мы позволяем
        посетителю узнать, с каким классом компонента он работает.
        """
        visitor.visit_concrete_component_a(self)
    def exclusive_method_of_concrete_component_a(self) -> str:
        """
        Конкретные Компоненты могут иметь особые методы, не объявленные в их
        базовом классе или интерфейсе. Посетитель всё же может использовать эти
        методы, поскольку он знает о конкретном классе компонента.
        """
        return "A"
class ConcreteComponentB(Component):
    def accept(self, visitor: Visitor):
        visitor.visit_concrete_component_b(self)
    def special_method_of_concrete_component_b(self) -> str:
        return "B"


class Visitor(ABC):
    """
    Интерфейс Посетителя объявляет набор методов посещения, соответствующих
    классам компонентов. Сигнатура метода посещения позволяет посетителю
    определить конкретный класс компонента, с которым он имеет дело.
    """
    @abstractmethod
    def visit_concrete_component_a(self, element: ConcreteComponentA): ...
    @abstractmethod
    def visit_concrete_component_b(self, element: ConcreteComponentB): ...
class ConcreteVisitorA(Visitor):
    def visit_concrete_component_a(self, element: ConcreteComponentA):
        print(f"ConcreteVisitorA -> {element.exclusive_method_of_concrete_component_a()}")
    def visit_concrete_component_b(self, element: ConcreteComponentB):
        print(f"ConcreteVisitorA -> {element.special_method_of_concrete_component_b()}")
class ConcreteVisitorB(Visitor):
    def visit_concrete_component_a(self, element: ConcreteComponentA):
        print(f"ConcreteVisitorB -> {element.exclusive_method_of_concrete_component_a()}")
    def visit_concrete_component_b(self, element: ConcreteComponentB):
        print(f"ConcreteVisitorB -> {element.special_method_of_concrete_component_b()}")


def client_code(components: list[Component], visitor: Visitor):
    for component in components:
        component.accept(visitor)


if __name__ == "__main__":
    components = [ConcreteComponentA(), ConcreteComponentB()]

    client_code(components, ConcreteVisitorA())
    client_code(components, ConcreteVisitorB())
    