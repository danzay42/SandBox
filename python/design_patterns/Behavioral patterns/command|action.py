# Применимость: Паттерн можно часто встретить в Python-коде, особенно когда нужно откладывать выполнение команд, выстраивать их в очереди, а также хранить историю и делать отмену.
# Признаки применения паттерна: Классы команд построены вокруг одного действия и имеют очень узкий контекст. Объекты команд часто подаются в обработчики событий элементов GUI. Практически любая реализация отмены использует принципа команд.

from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...


class SimpleCommand(Command):
    def __init__(self, payload: str) -> None:
        self._payload = payload
    def execute(self) -> None:
        print(f"SimpleCommand: {self._payload}")
class ComplexCommand(Command):
    def __init__(self, reciever: Receiver, a: str, b: str) -> None:
        self._receiver = reciever
        self._a = a
        self._b = b
    def execute(self) -> None:
        print(f"ComplexCommand: [{self._receiver.do_something(self._a)}] + [{self._receiver.do_something_else(self._b)}]")
    

class Receiver:
    def do_something(self, a: str):
        return f"Reciver: do_something with {a}"
    def do_something_else(self, b: str):
        return f"Reciver: do_something_else with {b}"

class Invoker:
    _on_start = None
    _on_finish = None
    def set_on_start(self, command: Command):
        self._on_start = command
    def set_on_finish(self, command: Command):
        self._on_finish = command
    def do_somthing_important(self):
        print("Invoker: Start")
        if isinstance(self._on_start, Command):
            self._on_start.execute()
        print("Invoker: Middle")
        if isinstance(self._on_finish, Command):
            self._on_finish.execute()
        print("Invoker: Finish")
    
if __name__ == '__main__':
    invoker = Invoker()
    invoker.set_on_start(SimpleCommand("Say Hi!"))
    invoker.set_on_finish(ComplexCommand(Receiver(), "Say By!", "P.S."))

    invoker.do_somthing_important()