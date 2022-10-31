# Применимость: Весь смысл использования Легковеса — в экономии памяти. Поэтому, если в приложении нет такой проблемы, то вы вряд ли найдёте там примеры Легковеса.
# Признаки применения паттерна: Легковес можно определить по создающим методам класса, которые возвращают закешированные объекты, вместо создания новых.

import json

class Flyweight:
    """
    Легковес хранит общую часть состояния (также называемую внутренним
    состоянием), которая принадлежит нескольким реальным бизнес-объектам.
    Легковес принимает оставшуюся часть состояния (внешнее состояние, уникальное
    для каждого объекта) через его параметры метода.
    """
    def __init__(self, shared_state: str) -> None:
        self._shared_state = shared_state
    def operation(self, unique_state: str) -> None:
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print(f"Flyweight: Displaying shared [{s}] and unique [{u}] state")

class FlyweightFactory:
    """
    Фабрика Легковесов создает объекты-Легковесы и управляет ими. Она
    обеспечивает правильное разделение легковесов. Когда клиент запрашивает
    легковес, фабрика либо возвращает существующий экземпляр, либо создает
    новый, если он ещё не существует.
    """
    _fliweights: dict[str, Flyweight] = {}
    
    def __init__(self, initial_flyweights: dict) -> None:
        for state in initial_flyweights:
            self._fliweights[self.get_key(state)] = Flyweight(state)
    
    def get_key(self, state: dict) -> str:
        """Возвращает хеш строки Легковеса для данного состояния."""
        return "_".join(sorted(state))
    
    def get_flyweight(self, shared_state: dict) -> Flyweight:
        """Возвращает существующий Легковес с заданным состоянием или создает новый."""
        key = self.get_key(shared_state)
        if not self._fliweights.get(key):
            print("FlyweightFactory: Can't find a flyweight, creating new one")
            self._fliweights[key] = Flyweight(shared_state)
        else:
            print("FlyweightFactory: Reusing exists flyweight")
        return self._fliweights[key]
    
    def list_flyweights(self):
        print(f"FlyweightFactory: I have {len(self._fliweights)} flyweights")
        print("\n".join(map(str, self._fliweights.keys())))


def add_car_to_police_database(factory: FlyweightFactory, plates: str, owner: str, brand: str, model: str, color: str):
    print("Add car to database")
    flyweight = factory.get_flyweight([brand, color, model])
    flyweight.operation([plates, owner])


if __name__ == "__main__":
    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])
    factory.list_flyweights()

    add_car_to_police_database(factory, "CL234IR", "James Doe", "BMW", "M5", "red")
    add_car_to_police_database(factory, "CL234IR", "James Doe", "BMW", "X1", "red")

    factory.list_flyweights()
