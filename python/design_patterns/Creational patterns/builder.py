# Строителя можно узнать в классе, который имеет один создающий метод и несколько методов настройки создаваемого продукта. Обычно, методы настройки вызывают для удобства цепочкой (например, someBuilder.setValueA(1).setValueB(2).create()).

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    """
    Интерфейс Строителя объявляет создающие методы для различных частей объектов
    Продуктов.
    """
    @property
    @abstractmethod
    def product(self) -> None: ...
    @abstractmethod
    def produce_part_a(self) -> None: ...
    @abstractmethod
    def produce_part_b(self) -> None: ...
    @abstractmethod
    def produce_part_c(self) -> None: ...

class ConcreteBuilder1(Builder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._product = Product1()
    def product(self) -> None:
        product = self._product
        self.reset()
        return product
    def produce_part_a(self) -> None:
        self._product.add("Part_A1")
    def produce_part_b(self) -> None:
        self._product.add("Part_B1")
    def produce_part_c(self) -> None:
        self._product.add("Part_C1")

class Product1:
    """
    Имеет смысл использовать паттерн Строитель только тогда, когда ваши продукты
    достаточно сложны и требуют обширной конфигурации.

    В отличие от других порождающих паттернов, различные конкретные строители
    могут производить несвязанные продукты. Другими словами, результаты
    различных строителей могут не всегда следовать одному и тому же интерфейсу.
    """
    def __init__(self) -> None:
        self.parts = []
    def add(self, part: Any) -> None:
        self.parts.append(part)
    def __str__(self) -> str:
        return str(self.parts)

class Director:
    """
    Директор отвечает только за выполнение шагов построения в определённой
    последовательности. Это полезно при производстве продуктов в определённом
    порядке или особой конфигурации. Строго говоря, класс Директор необязателен,
    так как клиент может напрямую управлять строителями.
    """
    def __init__(self) -> None:
        self._builder = None
    @property
    def builder(self) -> Builder:
        return self._builder
    @builder.setter
    def builder(self, builder: Builder):
        self._builder = builder
    def build_minimal(self):
        self.builder.produce_part_a()
    def build_maximum(self):
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()

if __name__ == "__main__":
    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder
    director.build_minimal()
    print(str(builder.product()))
    director.build_maximum()
    print(str(director.builder.product()))
    builder.produce_part_b()
    print(str(builder.product()))
