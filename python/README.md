# Docs
- [PEPS](https://peps.python.org/)
- [pypa](https://www.pypa.io/en/latest/)
- [pypa-projects](https://packaging.python.org/en/latest/key_projects/#pypa-projects)

## CheatSheets
- [pythoncheatsheet](https://www.pythoncheatsheet.org/)
- [mementopython3](https://perso.limsi.fr/pointal/_media/python:cours:mementopython3-english.pdf)

# Develop

## Libs

- datetime -> [pendulum](https://pendulum.eustace.io/)
- [result monada](https://github.com/rustedpy/result)
- [pypdf](https://pypdf2.readthedocs.io/en/3.0.0/)
- [python-dependency-injector](https://github.com/ets-labs/python-dependency-injector/)
- [dependency injection](https://github.com/sfermigier/awesome-dependency-injection-in-python)
- [distributed systems](https://github.com/bakwc/PySyncObj)
- [rust integration](https://github.com/PyO3/maturin)
- [cantok](https://github.com/pomponchik/cantok)

### print
- print
- pprint
- [icecream](https://github.com/gruns/icecream)
- [rich](https://github.com/Textualize/rich)
- [progress bar](https://github.com/tqdm/tqdm)
- logging
- [loguru](https://github.com/Delgan/loguru)

### decorators
- [retry](https://github.com/invl/retry)
- [cache,lru_cache](https://docs.python.org/3/library/functools.html)
- [deprecated](https://docs.python.org/3/library/warnings.html)
- [atexit](https://docs.python.org/3/library/atexit.html)

### asynchrony
- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [gevent](https://www.gevent.org/)

### cli framework
- [argparse](https://docs.python.org/3/library/argparse.html)
- [click](https://palletsprojects.com/p/click/)

### models
- NamedTuple
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [pydantic](https://docs.pydantic.dev/latest/)

### database abstraction
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLModel](https://sqlmodel.tiangolo.com/)

### message broker abstraction
- [Kombu](https://github.com/celery/kombu)

### data
- [numpy](https://numpy.org/)
- [scipy](https://scipy.org/)
- [pandas](https://pandas.pydata.org/)
- [polar](https://www.pola.rs/)
- [xarrays](https://github.com/pydata/xarray)
- [matplotlib](https://matplotlib.org/)
- [seaborn](https://seaborn.pydata.org/tutorial/introduction.html)

### http servers/clients
- [fastapi](https://fastapi.tiangolo.com/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [httpx](https://www.python-httpx.org/)
- [falcon](https://github.com/falconry/falcon) + [gevent](https://www.gevent.org/)

### config
- [dotenv](https://saurabh-kumar.com/python-dotenv/)
- [dynaconf](https://github.com/dynaconf/dynaconf)

### ui
- [textual](https://github.com/Textualize/textual)
- [textual-web](https://github.com/Textualize/textual-web)
- [flet](https://github.com/flet-dev/flet)

## Tools

### Interactive shells
- python
- bpython
- ipython
- [jupyter-notebook](https://jupyter.org/)

### environment
- [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [poetry](https://python-poetry.org/)
- [pyenv](https://github.com/pyenv/pyenv)

### formatters
isort + black

### linters
- pylint
- flake8
- ruff

### types
- [mypy](https://mypy.readthedocs.io/en/stable/)
- pyright

### tests
- [unittest](https://docs.python.org/3/library/unittest.html) + [pytest](https://docs.pytest.org/en/7.2.x/contents.html) + [tox](https://tox.wiki/en/latest/)
- [fakedb](https://github.com/emirozer/fake2db)
- [mimesis](https://github.com/lk-geimfari/mimesis)

### audit
- [safety](https://github.com/pyupio/safety)
- [pyscan](https://github.com/paulscherrerinstitute/pyscan)
- [pip-audit](https://github.com/pypa/pip-audit)

- [deptry](https://github.com/fpgmaas/deptry) - implicit dependency
- [vulture](https://github.com/jendrikseipp/vulture) - dead code
- [wily](https://github.com/tonybaloney/wily) - code simplicity
- [impulse](https://github.com/seddonym/impulse) - code graph

- [grimp](https://github.com/seddonym/grimp) - import control
- [import-linter](https://github.com/seddonym/import-linter) - import control wrapper
- [pytest-archon](https://github.com/jwbargsten/pytest-archon) - arch control

### documentation
- [Sphinx](https://www.sphinx-doc.org/en/master/)
- [Doxygen](https://www.doxygen.nl/manual/docblocks.html)

### build & publish
https://python-packaging.readthedocs.io/en/latest/#

- build: [hatch](https://github.com/pypa/hatch)
- publish: [twine](https://twine.readthedocs.io/en/stable/)
- [setup-py-upgrade](https://github.com/asottile/setup-py-upgrade)
- [setup-cfg-fmt](https://github.com/asottile/setup-cfg-fmt)

### compiler
[nuitka](https://nuitka.net/)
