from time import perf_counter
from typing import Callable, Any
from functools import wraps, partial
from dataclasses import dataclass


def time(fn: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        start = perf_counter()
        result = fn(*args, **kwargs)
        end = perf_counter()
        print(f"It's took {end-start}s")
        return result
    return wrapper


def logging1(name: str):
    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(name, "start", fn.__name__)
            result = fn(*args, **kwargs)
            print(name, "fin", fn.__name__)
            return result
        return wrapper
    return decorator


def logging2(fn, arg1: str, arg2: str) -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("logging2:", arg1, arg2)
        return fn(*args, **kwargs)
    return wrapper

default_logging2 = partial(logging2, arg1="arg111", arg2="arg222")


def logging3(fn = None, arg1: str = "default_1", arg2: str = "default_2") -> Callable[..., Any]:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("logging3:", arg1, arg2)
        return fn(*args, **kwargs)
    if fn:
        return wrapper
    return partial(logging3, arg1=arg1, arg2=arg2)
@time
@logging1("logging")
@default_logging2
@logging3
@logging3(arg1="arg123")
def function(in_: int) -> int:
    return 10 * in_



if __name__ == "__main__":
    print("result:", function(42))
