.ONESHELL:
.PHONY: install venv test clean
.DEFAULT_GOAL:=install

.make:
	mkdir .make
.make/venv:
	make venv
venv: .make
	virtualenv venv
	touch .make/venv

.make/install:
	make install
install: .make/venv .make
	pip install --upgrade pip poetry six
	poetry config virtualenvs.create false --local
	poetry install
	touch .make/install

.make/test:
	make test
test: .make/install
	pytest -vvv tests
	touch .make/test

requirements.txt:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

clean:
	rm -rf venv poetry.toml requirements.txt .pytest_cache .make __pycache__ .tox