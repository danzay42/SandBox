from geo import repository


def test_timezone_diff(tz1, tz2, res):
    assert repository.timezone_diff(tz1, tz2) == res




if __name__ == "__main__":
    res = timezone_diff("Europe/Moscow", "Asia/Tomsk")
    print(res)
    res = timezone_diff("US/Eastern", "Europe/Moscow")
    print(res)
    res = timezone_diff("Europe/Moscow", "Europe/Volgograd")
    print(res)
    res = timezone_diff("Europe/Moscow", "Europe/Paris")
    print(res)
    res = timezone_diff("Europe/Moscow", "Asia/Tomsk")
    print(res)


