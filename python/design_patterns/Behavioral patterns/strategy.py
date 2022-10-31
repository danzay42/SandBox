# Применимость: Стратегия часто используется в Python-коде, особенно там, где нужно подменять алгоритм во время выполнения программы. Многие примеры стратегии можно заменить простыми lambda-выражениями.
# Признаки применения паттерна: Класс делегирует выполнение вложенному объекту абстрактного типа или интерфейса.

from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    """
    Контекст хранит ссылку на один из объектов Стратегии. Контекст не знает
    конкретного класса стратегии. Он должен работать со всеми стратегиями
    через интерфейс Стратегии.
    """
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy
    @property
    def strategy(self) -> Strategy:
        return self._strategy
    @strategy.setter
    def strategy(self, strategy: Strategy):
        self._strategy = strategy
    def do_some_business_logic(self):
        print("Context: use unknown inner strategy")
        result = self._strategy.do_algorithm(["d", "c", "e", "b", "a"])
        print(",".join(result))


class Strategy(ABC):
    """
    Интерфейс Стратегии объявляет операции, общие для всех поддерживаемых версий
    некоторого алгоритма.

    Контекст использует этот интерфейс для вызова алгоритма, определённого
    Конкретными Стратегиями.
    """
    @abstractmethod
    def do_algorithm(self, data: list) -> list: ...


"""
Конкретные Стратегии реализуют алгоритм, следуя базовому интерфейсу Стратегии.
Этот интерфейс делает их взаимозаменяемыми в Контексте.
"""
class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data: list) -> list:
        return sorted(data)
class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data: list) -> list:
        return reversed(sorted(data))


if __name__ == "__main__":
    context = Context(ConcreteStrategyA())
    context.do_some_business_logic()
    context.strategy = ConcreteStrategyB()
    context.do_some_business_logic()

