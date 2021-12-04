
PYTHON=python
TARGET_FOLDERS=app tests

requirements:
	$(PYTHON) -m pip install -U pip wheel -r requirements.txt -r requirements-dev.txt

format_check:
	$(PYTHON) -m isort **/*.py -c
	$(PYTHON) -m black --check --diff -- $(TARGET_FOLDERS)

format:
	$(PYTHON) -m isort **/*.py
	$(PYTHON) -m black -- $(TARGET_FOLDERS)

lint:
	$(PYTHON) -m mypy --install-types --non-interactive -- $(TARGET_FOLDERS)
	$(PYTHON) -m flake8 -- $(TARGET_FOLDERS)
	$(PYTHON) -m pylint -- app

test:
	$(PYTHON) -m pytest -vv --doctest-modules -- $(TARGET_FOLDERS)

d_test:
	docker-compose run api make test

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

all: up format_check lint d_test down

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name '__pycache__' -delete
	rm -rf .mypy_cache .pytest_cache
	rm -rf dist

dist: clean
	mkdir dist
	zip -r -9 dist/alberto_contreras_plitix.zip -- $$(ls -a | grep --invert-match -E "venv|.vscode|.idea|.git$$|^\.+$$")
	tar cavf dist/alberto_contreras_plytix.tar.xz -- $$(ls -a | grep --invert-match -E "venv|.vscode|.idea|.git$$|^\.+$$")
