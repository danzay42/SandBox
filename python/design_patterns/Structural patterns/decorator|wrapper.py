# Применимость: Паттерн можно часто встретить в Python-коде, особенно в коде, работающем с потоками данных.
# Признаки применения паттерна: Декоратор можно распознать по создающим методам, которые принимают в параметрах объекты того же абстрактного типа или интерфейса, что и текущий класс.


class Component:
    def operation(self) -> str: ...


class ConcreteComponent(Component):
    def operation(self) -> str:
        return "ConcreteComponentOperation"


class Decorator(Component):
    """
    Базовый класс Декоратора следует тому же интерфейсу, что и другие
    компоненты. Основная цель этого класса - определить интерфейс обёртки для
    всех конкретных декораторов. Реализация кода обёртки по умолчанию может
    включать в себя поле для хранения завёрнутого компонента и средства его
    инициализации.
    """
    _component: Component = None
    def __init__(self, component: Component) -> None:
        self._component = component
    @property
    def component(self) -> Component:
        """Декоратор делегирует всю работу обёрнутому компоненту."""
        return self._component
    def operation(self) -> str:
        return self._component.operation()
class ConcreteDecoratorA(Decorator):
    def operation(self) -> str:
        return f"Wrapped with A[{self.component.operation()}]"
class ConcreteDecoratorB(Decorator):
    def operation(self) -> str:
        return f"Wrapped with B[{super().operation()}]"


def client_code(component: Component):
    print(component.operation())


if __name__ == "__main__":
    client_code(ConcreteComponent())
    client_code(ConcreteDecoratorA(ConcreteDecoratorB(ConcreteComponent())))