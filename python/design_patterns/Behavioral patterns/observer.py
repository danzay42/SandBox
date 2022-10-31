# Применимость: Наблюдатель можно часто встретить в Python коде, особенно там, где применяется событийная модель отношений между компонентами. Наблюдатель позволяет отдельным компонентам реагировать на события, происходящие в других компонентах.
# Признаки применения паттерна: Наблюдатель можно определить по механизму подписки и методам оповещения, которые вызывают компоненты программы.

from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange


class Subject(ABC):
    """Интерфейс издателя объявляет набор методов для управлениями подписчиками."""
    @abstractmethod
    def attach(self, observer: Observer): """Присоединяет наблюдателя к издателю."""
    @abstractmethod
    def detach(self, observer: Observer): """Отсоединяет наблюдателя от издателя."""
    @abstractmethod
    def notify(self): """Уведомляет всех наблюдателей о событии."""

class ConcreteSubject(Subject):
    _state: int = None
    _observers: list[Observer] = []
    def attach(self, observer: Observer):
        self._observers.append(observer)
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    def some_business_logic(self):
        self._state = randrange(0, 10)
        print(f"Subject: My state has just changed to: {self._state}")
        self.notify()


class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject): ...
class ConcreteObserverA(Observer):
    def update(self, subject: Subject):
        if subject._state < 3:
            print("ConcreteObserverA reacted!")
class ConcreteObserverB(Observer):
    def update(self, subject: Subject):
        if subject._state == 0 or subject._state >= 2:
            print("ConcreteObserverB reacted!")


if __name__ == "__main__":
    subject = ConcreteSubject()
    observer_a = ConcreteObserverA()
    observer_b = ConcreteObserverB()
    subject.attach(observer_a)
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()
    subject.some_business_logic()
