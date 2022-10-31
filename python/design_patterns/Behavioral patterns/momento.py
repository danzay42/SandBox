# Применимость: Снимок на Python чаще всего реализуют с помощью сериализации. Но это не единственный, да и не самый эффективный метод сохранения состояния объектов во время выполнения программы.

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits


class Momento(ABC):
    @abstractmethod
    def get_name(self) -> str: ...
    @abstractmethod
    def get_state(self) -> str: ...
class ConcreteMomento(Momento):
    def __init__(self, state: str) -> None:
        self._state = state
        self._date = str(datetime.now())[:19]
    def get_state(self) -> str:
        return self._state
    def get_name(self) -> str:
        return self._date
    

class Originator:
    """
    Создатель содержит некоторое важное состояние, которое может со временем
    меняться. Он также объявляет метод сохранения состояния внутри снимка и
    метод восстановления состояния из него.
    """
    _state = None
    """Для удобства состояние создателя хранится внутри одной переменной."""
    def __init__(self, state: str) -> None:
        self._state = state
        print(f"Originator: init {state=}")
    def do_something(self):
        """
        Бизнес-логика Создателя может повлиять на его внутреннее состояние.
        Поэтому клиент должен выполнить резервное копирование состояния с
        помощью метода save перед запуском методов бизнес-логики.
        """
        print("Originator: do changing...")
        self._state = self._generate_random_string(30)
        print(f"Originator: update state to: {self._state}")
    def _generate_random_string(self, length: int = 10):
        return "".join(sample(ascii_letters, length))
    def save(self) -> Momento:
        """Сохраняет текущее состояние внутри снимка."""
        return ConcreteMomento(self._state)
    def restore(self, momento: Momento):
        self._state = momento.get_state()
        print(f"Originator: restore state to: {self._state}")
    def __str__(self) -> str:
        return self._state


class Caretaker:
    """
    Опекун не зависит от класса Конкретного Снимка. Таким образом, он не имеет
    доступа к состоянию создателя, хранящемуся внутри снимка. Он работает со
    всеми снимками через базовый интерфейс Снимка.
    """
    def __init__(self, originator: Originator) -> None:
        self._momentos: list[Momento] = []
        self._originator = originator
    def backup(self):
        print("Caretaker: Make Backup")
        self._momentos.append(self._originator.save())
    def undo(self):
        if not self._momentos:
            return
        momento = self._momentos.pop()
        print("Caretaker: Make Undo")
        try:
            self._originator.restore(momento)
        except Exception:
            self.undo()
    def show_history(self):
        for momento in self._momentos:
            print(momento.get_name(), momento.get_state())
    

if __name__ == "__main__":
    originator = Originator("Foo-Bar-Tar-Far")
    caretaker = Caretaker(originator)

    caretaker.backup()
    originator.do_something()
    caretaker.backup()
    originator.do_something()
    caretaker.backup()
    originator.do_something()

    print()
    caretaker.show_history()
    caretaker.undo()
    caretaker.undo()
    caretaker.undo()

    print(originator)
