# virtualenv_wrapper compatible names
VIRTUALENVWRAPPER_VIRTUALENV?=virtualenv
VIRTUAL_ENV?=venv

PYTHON=$(VIRTUAL_ENV)/bin/python
PIP=$(VIRTUAL_ENV)/bin/pip
COVERAGE=$(VIRTUAL_ENV)/bin/coverage

$(PYTHON):
	$(VIRTUALENV) $(VIRTUAL_ENV)

$(COVERAGE): virtualenv
	$(PIP) install coverage

virtualenv: $(PYTHON)

dev_requirements:
	$(PIP) install -r dev_requirements.txt

install:
	$(PYTHON) setup.py install
	$(PYTHON) manage.py syncdb --noinput

develop: dev_requirements
	$(PYTHON) setup.py develop
	$(PYTHON) manage.py syncdb --noinput

$(FLAKE8): virtualenv
	$(PIP) install flake8

test: develop flake8
	$(PYTHON) manage.py test frontend

coverage: develop
	$(COVERAGE) run --branch --source=. manage.py test frontend
	$(COVERAGE) report -m

start: $(PROC) .env
	$(PROC) start -f $(PROCFILE)

backup:
	#TODO

flake8: $(FLAKE8)
	flake8 .
