# Паттерн можно определить по методам, принимающем фабрику, которая, в свою очередь, используется для создания конкретных продуктов, возвращая их через абстрактные типы или интерфейсы.

from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    """
    Интерфейс Абстрактной Фабрики объявляет набор методов, которые возвращают
    различные абстрактные продукты. Эти продукты называются семейством и связаны
    темой или концепцией высокого уровня. Продукты одного семейства обычно могут
    взаимодействовать между собой. Семейство продуктов может иметь несколько
    вариаций, но продукты одной вариации несовместимы с продуктами другой.
    """
    @abstractmethod
    def create_product_a(self) -> AbstractProductA: ...
    @abstractmethod
    def create_product_b(self) -> AbstractProductB: ...

class ConcreteFactory1(AbstractFactory):
    """
    Конкретная Фабрика производит семейство продуктов одной вариации. Фабрика
    гарантирует совместимость полученных продуктов. Обратите внимание, что
    сигнатуры методов Конкретной Фабрики возвращают абстрактный продукт, в то
    время как внутри метода создается экземпляр конкретного продукта.
    """
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()
    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()
class ConcreteFactory2(AbstractFactory):
    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()
    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


class AbstractProductA(ABC):
    """
    Каждый отдельный продукт семейства продуктов должен иметь базовый интерфейс.
    Все вариации продукта должны реализовывать этот интерфейс.
    """
    @abstractmethod
    def function_a(self) -> str: ...
class ConcreteProductA1(AbstractProductA):
    def function_a(self) -> str:
        return "A1"
class ConcreteProductA2(AbstractProductA):
    def function_a(self) -> str:
        return "A2"

class AbstractProductB(ABC):
    """
    Каждый отдельный продукт семейства продуктов должен иметь базовый интерфейс.
    Все вариации продукта должны реализовывать этот интерфейс.
    """
    @abstractmethod
    def function_b(self) -> str: ...
class ConcreteProductB1(AbstractProductB):
    def function_b(self) -> str:
        return "B1"
class ConcreteProductB2(AbstractProductB):
    def function_b(self) -> str:
        return "B2"


def client_code(factory: AbstractFactory) -> None:
    print("-"*60)
    print(factory.create_product_a().function_a())
    print(factory.create_product_b().function_b())

if __name__ == "__main__":
    client_code(ConcreteFactory1())
    client_code(ConcreteFactory2())
