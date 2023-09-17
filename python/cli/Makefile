.ONESHELL:
.PHONY: venv install test tox format static clean
.DEFAULT_GOAL:=install

source = src tests

venv:
	python -m venv .venv

install:
	python -m pip install --upgrade pip six poetry
	poetry install

test:
	pytest -vvv tests

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

tox:
	tox p -- -vvv

format: $(source)
	black $^

static: $(source)
	ruff $^
	mypy $^
	flake8 $^
	pylint $^

clean:
	#rm -rf .venv __pycache__
	rm -rf .*_cache .tox
	rm -rf dist
	rm -rf requirements.txt