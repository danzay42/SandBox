import dataclasses
from datetime import datetime
from typing import Callable, Protocol
from functools import partial

FuncType = Callable[[str, str, str], str]
Transaction = tuple[str, datetime, int]


class MyClass(Protocol):
    def __call__(self, a: str, b: str, c: str) -> str:
        ...


class MyArgs(Protocol):
    @property
    def a(self) -> str:
        ...

    @property
    def c(self) -> str:
        ...


@dataclasses.dataclass
class Args:
    a: str
    b: str
    c: str
    d: str


def my_func(a: str, b: str, c: str) -> str:
    return a + b + c


def main1(func: FuncType):
    print("main1", func("hello", "world", "!"))


def main2(func: MyClass):
    print("main2", func("hello", "world", "!"))


def main3(args: MyArgs):
    p_func = partial(my_func, a=args.a, c=args.c)
    print(p_func(b="Doom1"))
    print(p_func(b="Doom2"))


if __name__ == '__main__':
    main1(my_func)
    main2(my_func)
    main3(Args(a="Hello ", b="...", c="!", d="..."))
