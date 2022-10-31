class MyObject:
    def __init__(self, parameters) -> None:
        self.parameters = parameters
    def __str__(self) -> str:
        return str(self.parameters)

class MyObjectFactory:
    def create_object_type_1(self):
        params = ["1","2", "3"]
        return MyObject(params)
    def create_object_type_2(self):
        params = [4,5,6]
        return MyObject(params)
    def create_object_type_3(self):
        params = ["one", "two", "three"]
        return MyObject(params)

factory = MyObjectFactory()
print(factory.create_object_type_1())
print(factory.create_object_type_2())
print(factory.create_object_type_3())