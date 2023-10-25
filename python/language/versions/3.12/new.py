# new f-strings
print(f"Hello {"World"}")
print(f"Hello {",".join([
    "1",
    "2",
    "3",
])}")


# **kwargs type
from typing import TypedDict, Unpack

class MyClass(TypedDict):
    foo: str
    bar: int

def my_func(**kwargs: Unpack[MyClass]):
    print(kwargs)

my_func(foo="foo", bar=123)


# Generics [T], [T, B, C], [T, *Ts], [T, **Tk], [T: (float, int)]
def my_gen_fn[T: str](foo: T, bar: T) -> T:
    return foo + "_" + bar

print(my_gen_fn("a", "b"))


# type alias
type MyType = float

def my_alias(var: MyType):
    print("MyType var value: ", str(var))

my_alias(123.)


# pathlib update
from pathlib import Path

for res in Path("./python/language/versions/3.12").walk():
    print(res)


# itertools flatten
from itertools import batched

for batch in batched(range(10), 3):
    print(batch)