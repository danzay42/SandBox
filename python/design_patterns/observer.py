class ObservedObject:
    def __init__(self, name):
        self.name = name
        self.observers = []
    def add_observer(self, observer):
        self.observers.append(observer)
    def notify_observers(self, event):
        for observer in self.observers:
            observer.send_notification(self.name, event)

class Observer:
    def __init__(self, name) -> None:
        self.name = name
    def send_notification(self, from_, event):
        print(f"[{self.name}]Get notification {from_=} {event=}")

my_object = ObservedObject("observed_object")
my_object.add_observer(Observer(1))
my_object.add_observer(Observer(2))
my_object.add_observer(Observer(3))

my_object.notify_observers("!event!")