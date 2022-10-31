# Применимость: Паттерн часто встречается в клиентских приложениях, написанных на Python, которые используют классы-фасады для упрощения работы со сложными библиотеки или API.
# Признаки применения паттерна: Фасад угадывается в классе, который имеет простой интерфейс, но делегирует основную часть работы другим классам. Чаще всего, фасады сами следят за жизненным циклом объектов сложной системы.

from __future__ import annotations


class Facade:
    def __init__(self, subsystem_1: Subsystem1, subsystem_2: Subsystem2) -> None:
        self._subsystem_1 = subsystem_1
        self._subsystem_2 = subsystem_2
    def operation(self) -> str:
        results = [
            "Initialize",
            self._subsystem_1.operation_a(),
            self._subsystem_2.operation_x(),
            "Work",
            self._subsystem_1.operation_b(),
            self._subsystem_2.operation_y(),
            "Fin"
        ]
        return "\n".join(results)


class Subsystem1:
    def operation_a(self) -> str:
        return "Subsystem 1 - RDY!"
    def operation_b(self) -> str:
        return "Subsystem 1 - GO!"
class Subsystem2:
    def operation_x(self) -> str:
        return "Subsystem 2 - RDY!"
    def operation_y(self) -> str:
        return "Subsystem 2 - GO!"


def client_code(facade: Facade):
    print(facade.operation())


if __name__ == "__main__":
    client_code(Facade(Subsystem1(), Subsystem2()))
