class MyObject:
    def __init__(self) -> None:
        self.property_1 = "-"
        self.property_2 = "-"
        self.property_3 = "-"
    def set_prop_1(self, prop="+"):
        self.property_1 = prop
    def set_prop_2(self, prop="+"):
        self.property_2 = prop
    def set_prop_3(self, prop="+"):
        self.property_3 = prop
    def __str__(self) -> str:
        return str(self.property_1+self.property_2+self.property_3)

class MyObjectBuilder:
    def __init__(self) -> None:
        self.my_object = MyObject()
    def add_prop_1(self, prop):
        self.my_object.set_prop_1(prop)
        return self
    def add_prop_2(self, prop):
        self.my_object.set_prop_2(prop)
        return self
    def add_prop_3(self, prop):
        self.my_object.set_prop_3(prop)
        return self
    def build(self):
        return self.my_object

print(MyObjectBuilder().add_prop_1("+").build())
print(MyObjectBuilder().add_prop_1("+").add_prop_2("+").build())
print(
    MyObjectBuilder()
        .add_prop_1("+")
        .add_prop_2("+")
        .add_prop_3("+")
        .build()
)