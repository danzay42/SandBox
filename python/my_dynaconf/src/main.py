from config import settings


def main():
    print(f"{settings.host=}")
    print(f"{settings.port=}")
    print(f"{settings.login=}")
    print(f"{settings.password=}")


if __name__ == '__main__':
    main()
