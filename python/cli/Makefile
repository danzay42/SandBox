.ONESHELL:
.PHONY: venv install test clean
.DEFAULT_GOAL:=install

venv:
	python -m venv .venv

install:
	python -m pip install --upgrade pip poetry
	poetry install

test:
	pytest -vvv tests

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

clean:
	rm -rf .venv __pycache__
	rm -rf .*_cache
	rm -rf requirements.txt