# Управление "фонариком" с помощью сервера поверх TCP-соединения:
Для работы пакета нужен python>=3.10, pip
## Установка
linux: ```pip install flashlight-0.1.1-py3-none-any.whl```
win: ```pip install .\flashlight-0.1.1-py3-none-any.whl```
## Запуск
linux: ```flashlight```
win: ```flashlight.exe```
## Удаление
```pip uninstall flashlight```
## Сборка из исходников
Для сборки пакета из репозитория используется пакетный менеджер poetry:
### Сборка пакета
```
pip install poetry
git clone https://github.com/danzay42/flashlight
cd flashlight
poetry build
```
результат сборки будет помещен в папку dist
### Запуск кода без сборки
```poetry run flashlight```
