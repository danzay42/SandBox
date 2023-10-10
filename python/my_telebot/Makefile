.ONESHELL:
.PHONY: install test tox format static clean
.DEFAULT_GOAL:=install

source = src tests

venv:
	virtualenv venv

install:
	pip install --upgrade pip poetry
	poetry install

test:
	pytest -vvv --tb=no tests

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

format: $(source)
	black $^

static: $(source)
	ruff $^
	mypy $^
	flake8 $^
	pylint $^

docker:
	docker run --rm -p 5050:80 \
	  -e PGADMIN_DEFAULT_EMAIL=root@root.com \
	  -e PGADMIN_DEFAULT_PASSWORD=root \
	  -d dpage/pgadmin4
	#  -e PGADMIN_CONFIG_SERVER_MODE=False

clean:
	rm -rf .venv __pycache__
	rm -rf .*_cache .tox
	rm -rf dist
	rm -rf requirements.txt