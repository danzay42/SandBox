from typing import Self, LiteralString


class Singletone:
    def __new__(cls: type[Self]) -> Self:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singletone, cls).__new__(cls)
        return cls.instance


s1 = Singletone()
s2 = Singletone()
print(f"{s1 is s2 = }")


def work_with_external_string(string: LiteralString):
    print("This is external string: ", string)

work_with_external_string("malware string exec")
work_with_external_string(input()) # for example exteranl sql request
