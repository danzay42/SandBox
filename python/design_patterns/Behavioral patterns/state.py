# Применимость: Паттерн Состояние часто используют в Python для превращения в объекты громоздких стейт-машин, построенных на операторах switch.
# Признаки применения паттерна: Методы класса делегируют работу одному вложенному объекту.

from __future__ import annotations
from abc import ABC, abstractmethod


class Context:
    _state = None
    def __init__(self, state: State) -> None:
        self.transition_to(state)
    def transition_to(self, state: State):
        print(f"Context: change state to {type(state).__name__}")
        self._state = state
        self._state.context = self
    def request_1(self):
        self._state.handle_1()
    def request_2(self):
        self._state.handle_2()


class State(ABC):
    _context: Context
    @property
    def context(self) -> Context:
        return self._context
    @context.setter
    def context(self, context: Context):
        self._context = context
    @abstractmethod
    def handle_1(self): ...
    @abstractmethod
    def handle_2(self): ...


class ConcreteStateA(State):
    def handle_1(self):
        print("ConcreteStateA: handle_1")
        self.context.transition_to(ConcreteStateB())
    def handle_2(self):
        print("ConcreteStateA: handle_2")
class ConcreteStateB(State):
    def handle_1(self):
        print("ConcreteStateB: handle_1")
    def handle_2(self):
        print("ConcreteStateB: handle_2")
        self.context.transition_to(ConcreteStateA())


if __name__ == "__main__":
    context = Context(ConcreteStateA())
    context.request_1()
    context.request_2()