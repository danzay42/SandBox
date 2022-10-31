# Применимость: Паттерн Мост особенно полезен когда вам приходится делать кросс-платформенные приложения, поддерживать несколько типов баз данных или работать с разными поставщиками похожего API (например, cloud-сервисы, социальные сети и т. д.)
# Признаки применения паттерна: Если в программе чётко выделены классы «управления» и несколько видов классов «платформ», причём управляющие объекты делегируют выполнение платформам, то можно сказать, что у вас используется Мост.

from __future__ import annotations
from abc import ABC, abstractmethod


class Abstraction:
    """
    Абстракция устанавливает интерфейс для «управляющей» части двух иерархий
    классов. Она содержит ссылку на объект из иерархии Реализации и делегирует
    ему всю настоящую работу.
    """
    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation
    def operation(self) -> str:
        return f"Abstraction[{self.implementation.opertion_implementation()}]"
class ExtendedAbstraction(Abstraction):
    """
    Можно расширить Абстракцию без изменения классов Реализации.
    """
    def operation(self) -> str:
        return f"ExtendedAbstraction[{self.implementation.opertion_implementation()}]"


class Implementation(ABC):
    """
    Реализация устанавливает интерфейс для всех классов реализации. Он не должен
    соответствовать интерфейсу Абстракции. На практике оба интерфейса могут быть
    совершенно разными. Как правило, интерфейс Реализации предоставляет только
    примитивные операции, в то время как Абстракция определяет операции более
    высокого уровня, основанные на этих примитивах.
    """
    @abstractmethod
    def opertion_implementation(self) -> str: ...
"""
Каждая Конкретная Реализация соответствует определённой платформе и реализует
интерфейс Реализации с использованием API этой платформы.
"""
class ConcreteImplementationA(Implementation):
    def opertion_implementation(self) -> str:
        return "Implementation A"
class ConcreteImplementationB(Implementation):
    def opertion_implementation(self) -> str:
        return "Implementation B"


def client_code(abstraction: Abstraction):
    print(abstraction.operation())


if __name__ == "__main__":
    client_code(Abstraction(ConcreteImplementationA()))
    client_code(ExtendedAbstraction(ConcreteImplementationB()))
