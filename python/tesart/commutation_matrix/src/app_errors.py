class MatrixError(Exception):
    """
    Error description
    """
    message = None
    code = None

    def __str__(self):
        return f"Matrix Error: [{self.code}, {self.message}]\n" \
               f"{self.__doc__.rstrip()}"
    
    def __repr__(self):
        return f"{self.code}, {self.message}"


class NoError(MatrixError):
    """
    Ошибок нет, система работает нормально.
    """
    message = 'No Error'
    code = 0


class WrongCommand(MatrixError):
    """
    Некорректная команда.
    """
    message = 'Wrong Command'
    code = 1


class WrongParameter(MatrixError):
    """
    Некорректный параметр.
    """
    message = 'Wrong Parameter'
    code = 2


class ParameterOutOfRange(MatrixError):
    """
    Параметр выходит за диапазон максимальных значений установки параметра.
    """
    message = 'Parameter Out Of Range'
    code = 3


class OutputBusy(MatrixError):
    """
    Возникает при попытке переключить вход матрицы коммутации на уже задействованный выход.
    """
    message = 'Output Busy'
    code = 4


class ErrorTransferData(MatrixError):
    """
    Ошибка передачи пакета данных. Внутренняя ошибка, возникает при сбоях в системе.
    """
    message = 'Error Transfer Data'
    code = 5


class NoSwitchStatus(MatrixError):
    """
    Нет данных о состояние переключателей. Внутренняя ошибка, возникает при сбоях в системе.
    """
    message = 'Tx Data Error'
    code = 6
