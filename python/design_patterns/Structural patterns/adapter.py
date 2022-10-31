# Адаптер получает конвертируемый объект в конструкторе или через параметры своих методов. Методы Адаптера обычно совместимы с интерфейсом одного объекта. Они делегируют вызовы вложенному объекту, превратив перед этим параметры вызова в формат, поддерживаемый вложенным объектом.


class Target:
    def request(self) -> str:
        return "Target Request"

class Adaptee:
    def specific_request(self) -> str:
        return "Specific Request"
    
class Adapter1(Target, Adaptee):
    def request(self) -> str:
        return f"{self.specific_request()} -> Target Request"

class Adapter2(Target):
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
    def request(self) -> str:
        return f"{self.adaptee.specific_request()} -> Target Request"

def client_code(target: Target):
    print(target.request())

if __name__ == "__main__":
    client_code(Target())
    client_code(Adapter1())
    client_code(Adapter2(Adaptee()))
