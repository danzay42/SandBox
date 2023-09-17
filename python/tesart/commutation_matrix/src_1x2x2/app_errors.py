from src.app_errors import *


class ErrorTransferData(ErrorTransferData):
    """
    Ошибка передачи пакета данных. Внутренняя ошибка, возникает при сбоях в системе.
    """
    message = 'Error Transfer Data'
    code = 4


class NoSwitchStatus(NoSwitchStatus):
    """
    Нет данных о состояние переключателей. Внутренняя ошибка, возникает при сбоях в системе.
    """
    message = 'No Switch Status'
    code = 5
