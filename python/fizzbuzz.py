def var1():
    def fizzbuzz(num: int) -> str | int:
        res = ""
        if num % 3 == 0:
            res += "fizz"
        if num % 5 == 0:
            res += "buzz"
        return res or num

    print(list(map(fizzbuzz, range(100))))


def var2():
    print(list(map(lambda i: (("fizz" if i % 3 == 0 else '') + ("buzz" if i % 5 == 0 else '')) or i, range(100))))


def var3():
    print(['fizz' * (i % 3 == 0) + 'buzz' * (i % 5 == 0) or i for i in range(100)])


var1()
var2()
var3()
