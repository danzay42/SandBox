# Применимость: Шаблонные методы можно встретить во многих библиотечных классах Python. Разработчики создают их, чтобы позволить клиентам легко и быстро расширять стандартный код при помощи наследования.
# Признаки применения паттерна: Класс заставляет своих потомков реализовать методы-шаги, но самостоятельно реализует структуру алгоритма.

from abc import ABC, abstractmethod


class AbstractClass(ABC):
    """
    Абстрактный Класс определяет шаблонный метод, содержащий скелет некоторого
    алгоритма, состоящего из вызовов (обычно) абстрактных примитивных операций.

    Конкретные подклассы должны реализовать эти операции, но оставить сам
    шаблонный метод без изменений.
    """

    def template_method(self):
        """Шаблонный метод определяет скелет алгоритма."""
        self.base_operation_1()
        self.required_operation_1()
        self.hook_1()
        self.base_operation_2()
        self.required_operation_2()
        self.hook_2()
        self.base_operation_3()
    # Эти операции уже имеют реализации.
    def base_operation_1(self):
        print("\nBase Operation 1")
    def base_operation_2(self):
        print("Base Operation 2")
    def base_operation_3(self):
        print("Base Operation 3\n")
     # А эти операции должны быть реализованы в подклассах.
    @abstractmethod
    def required_operation_1(self): ...
    @abstractmethod
    def required_operation_2(self): ...
    # Это «хуки». Подклассы могут переопределять их, но это не обязательно,
    # поскольку у хуков уже есть стандартная (но пустая) реализация. Хуки
    # предоставляют дополнительные точки расширения в некоторых критических
    # местах алгоритма.
    def hook_1(self): ...
    def hook_2(self): pass


class ConcreteClassA(AbstractClass):
    def required_operation_1(self):
        print("Concrete A Required 1")
    def required_operation_2(self):
        print("Concrete A Required 2")
class ConcreteClassB(AbstractClass):
    def required_operation_1(self):
        print("Concrete B Required 1")
    def required_operation_2(self):
        print("Concrete B Required 2")


def client_code(abstract_class: AbstractClass):
    abstract_class.template_method()


if __name__ == "__main__":
    client_code(ConcreteClassA())
    client_code(ConcreteClassB())