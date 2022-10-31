def first_version():
    class MySingleton:
        instance = None
        def __new__(cls, *args, **kwargs):
            if cls.instance is None:
                instance = super().__new__(cls)
                cls.instance = instance
            return cls.instance


    s1 = MySingleton()
    s2 = MySingleton()

    if id(s1) == id(s2):
        print("is Singletone")
    else:
        print("is't Singletone")

def better_version():
    class Singleton(type):
        _instances = {}
        def __call__(self, *args, **kwds):
            if self not in self._instances:
                self._instances[self] = super(Singleton, self).__call__(*args, **kwds)
            return self._instances[self]

    class Logger(metaclass=Singleton):
        def log(self, msg):
            print(msg)
    
    i1 = Logger()
    i2 = Logger()

    print(i1)
    print(i2)
    print(f"{id(i1) == id(i2)}")

better_version()