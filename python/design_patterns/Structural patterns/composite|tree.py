# Применимость: Паттерн Компоновщик встречается в любых задачах, которые связаны с построением дерева. Самый простой пример — составные элементы GUI, которые тоже можно рассматривать как дерево.
# Признаки применения паттерна: Если из объектов строится древовидная структура, и со всеми объектами дерева, как и с самим деревом работают через общий интерфейс.

from __future__ import annotations
from abc import ABC, abstractmethod


class Component(ABC):
    @property
    def parent(self) -> Component:
        return self._parent
    @parent.setter
    def parent(self, parent: Component):
        self._parent = parent
    def add(self, component: Component): ...
    def remove(self, component: Component): ...
    def is_composite(self) -> bool: return False
    @abstractmethod
    def operation(self) -> str: ...


class Leaf(Component):
    def operation(self) -> str:
        return "Leaf"

    
class Tree(Component):
    def __init__(self) -> None:
        self._children: list[Component] = []
    def add(self, component: Component): 
        self._children.append(component)
        component.parent = self
    def remove(self, component: Component):
        self._children.remove(component)
        component.parent = None
    def is_composite(self) -> bool: return True
    def operation(self) -> str: 
        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Branch({'+'.join(results)})"


def client_code(component: Component):
    print(f"Result: {component.operation()}")

def client_code_2(component_1: Component, component_2: Component):
    if component_1.is_composite():
        component_1.add(component_2)
    print(f"Result: {component_1.operation()}")


if __name__ == "__main__":
    leaf = Leaf()
    client_code(leaf)

    tree = Tree()
    branch_1 = Tree()
    branch_1.add(Leaf())
    branch_1.add(Leaf())
    branch_2 = Tree()
    branch_2.add(Leaf())
    tree.add(branch_1)
    tree.add(branch_2)

    client_code(tree)
    client_code_2(tree, leaf)
