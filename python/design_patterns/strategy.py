from abc import ABC, abstractclassmethod

class FilterStrategy(ABC):
    @abstractclassmethod
    def check_values(self, val): ...

class RemoveNegative(FilterStrategy):
    def check_values(self, val):
        return val < 0
class RemoveOdd(FilterStrategy):
    def check_values(self, val):
        return abs(val) % 2

class Values:
    def __init__(self, vals) -> None:
        self.vals = vals
    def filter(self, strategy):
        return [val for val in self.vals if not strategy.check_values(val)]

print(Values([-7, -4, -1, 0, 2, 6, 9]).filter(RemoveOdd()))
print(Values([-7, -4, -1, 0, 2, 6, 9]).filter(RemoveNegative()))