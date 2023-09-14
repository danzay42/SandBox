.ONESHELL:

install venv:
	virtualenv venv
	. venv/bin/activate
	pip install --upgrade pip poetry six
	poetry config virtualenvs.create false --local
	poetry install

requirements:
	. venv/bin/activate
	poetry export -f requirements.txt --output requirements.txt --without-hashes

test: venv
	. venv/bin/activate
	pytest -vvv tests

clean:
	rm -rf venv poetry.toml requirements.txt .pytest_cache