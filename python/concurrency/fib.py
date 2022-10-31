# https://www.youtube.com/watch?v=MCs5OvhV9S4


def fib(n):
    if n <= 2:
        return 1
    else:
        return fib(n-1)+fib(n-2)