
PYTHON=python

requirements:
	$(PYTHON) -m pip install -U pip wheel -r requirements.txt -r requirements.dev.txt

test:
	$(PYTHON) -m pytest -vv --doctest-modules -- app tests
