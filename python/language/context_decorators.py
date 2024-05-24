import contextlib
import functools
import time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timing(name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            t0 = time.monotonic()
            try:
                return func(*args, **kwargs)
            finally:
                t1 = time.monotonic()
                print(f"LOG: {name} took: {t1 - t0}")

        return wrapper

    return decorator


@contextlib.contextmanager
def timing_ctx(name: str):
    t0 = time.monotonic()
    try:
        yield
    finally:
        t1 = time.monotonic()
        print(f"LOG: {name} took: {t1 - t0}")


@timing("decorator.timing")
def d(x: int) -> int:
    return x * x


@timing_ctx("ctx.timing")
def c(x: int) -> int:
    return x * x


d(10)
c(10)
