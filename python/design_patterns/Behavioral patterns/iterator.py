# Применимость: Паттерн можно часто встретить в Python-коде, особенно в программах, работающих с разными типами коллекций, и где требуется обход разных сущностей.
# Признаки применения паттерна: Итератор легко определить по методам навигации (например, получения следующего/предыдущего элемента и т. д.). Код использующий итератор зачастую вообще не имеет ссылок на коллекцию, с которой работает итератор. Итератор либо принимает коллекцию в параметрах конструктора при создании, либо возвращается самой коллекцией.


from __future__ import annotations
from collections.abc import Iterable, Iterator
from typing import Any, List

"""
Для создания итератора в Python есть два абстрактных класса из встроенного
модуля collections - Iterable, Iterator. Нужно реализовать метод __iter__() в
итерируемом объекте (списке), а метод __next__() в итераторе.
"""

class AlabeticalOrederIterator(Iterator):
    """Конкретные Итераторы реализуют различные алгоритмы обхода. Эти классы
    постоянно хранят текущее положение обхода."""
    _position: int = None
    """Атрибут _position хранит текущее положение обхода. У итератора может быть
    множество других полей для хранения состояния итерации, особенно когда он
    должен работать с определённым типом коллекции."""
    _reverse: bool = False
    """Этот атрибут указывает направление обхода."""
    def __init__(self, collection: WordsCollection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0
    def __next__(self):
        """
        Метод __next __() должен вернуть следующий элемент в последовательности.
        При достижении конца коллекции и в последующих вызовах должно вызываться
        исключение StopIteration.
        """
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
            return value
        except IndexError:
            raise StopIteration()
    

class WordsCollection(Iterable):
    """
    Конкретные Коллекции предоставляют один или несколько методов для получения
    новых экземпляров итератора, совместимых с классом коллекции.
    """
    def __init__(self, collection: list[Any] = []) -> None:
        self._collection = collection
    def __iter__(self) -> AlabeticalOrederIterator:
        """
        Метод __iter__() возвращает объект итератора, по умолчанию мы возвращаем
        итератор с сортировкой по возрастанию.
        """
        return AlabeticalOrederIterator(self._collection)
    def get_reverse_iterator(self) -> AlabeticalOrederIterator:
        return AlabeticalOrederIterator(self._collection, reverse=True)
    def add_item(self, item: Any):
        self._collection.append(item)


if __name__ == "__main__":
    collection = WordsCollection()
    collection.add_item("First")
    collection.add_item("Second")
    collection.add_item("Third")

    print("Straight traversal:")
    print("\n".join(collection))
    print()

    print("Reverse traversal:")
    print("\n".join(collection.get_reverse_iterator()))
