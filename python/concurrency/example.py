def gen(n):
    for i in range(n):
        print(i)
        yield

    print("this is the end")



g1 = gen(10)
g2 = gen(5)
