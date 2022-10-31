# Применимость: Паттерн Заместитель применяется в Python коде тогда, когда надо заменить настоящий объект его суррогатом, причём незаметно для клиентов настоящего объекта. Это позволит выполнить какие-то добавочные поведения до или после основного поведения настоящего объекта.
# Признаки применения паттерна: Класс заместителя чаще всего делегирует всю настоящую работу своему реальному объекту. Заместители часто сами следят за жизненным циклом своего реального объекта.

from abc import ABC, abstractmethod


class Subject(ABC):
    @abstractmethod
    def request(self): ...


class RealSubject(Subject):
    def request(self):
        print("Real Subject: Handling Request...")
    

class Proxy(Subject):
    def __init__(self, real_subject: RealSubject) -> None:
        self._real_subject = real_subject
    def request(self):
        if self.check_access():
            self._real_subject.request()
            self.log_access()
    def check_access(self) -> bool:
        print("Proxy: Check Access")
        return True
    def log_access(self):
        print("Proxy: Logging")


def client_code(subject: Subject):
    subject.request()


if __name__ == "__main__":
    client_code(RealSubject())
    client_code(Proxy(RealSubject()))