

exception_group = ExceptionGroup("Моя группа исключений", [
        ValueError("Ошибка Значения"),
        TypeError("Ошибка Типа"),
        IndexError("Ошибка Индекса"),
        ValueError("Ошибка Значения, еще одна"),
        ])


try:
    raise exception_group
except* ValueError as eg:
    for exc in eg.exceptions:
        print(f"Поймал ошибку значения: {exc}")
except* TypeError as eg:
    for exc in eg.exceptions:
        print(f"Поймал ошибку типа: {exc}")
except* Exception as eg:
    for exc in eg.exceptions:
        print(f"Поймал все типы ошибки: {exc}")


raise exception_group
