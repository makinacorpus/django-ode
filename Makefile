
# virtualenv_wrapper compatible names
VIRTUALENVWRAPPER_VIRTUALENV?=virtualenv
VIRTUAL_ENV?=venv
NPM?=npm
GRUNT?=grunt

PYTHON=$(VIRTUAL_ENV)/bin/python
PIP=$(VIRTUAL_ENV)/bin/pip
COVERAGE=$(VIRTUAL_ENV)/bin/coverage
OMIT='./salt/*,./node-v0.10.22-linux-x64/,./django_ode/settings/local.py,./src,.tox,*/migrations/*'
TEST_COMMAND=manage.py test --settings=django_ode.settings.base frontend accounts dashboard
COLLECT_STATIC=python manage.py collectstatic --noinput

$(PYTHON):
	$(VIRTUALENV) $(VIRTUAL_ENV)

virtualenv: $(PYTHON)

dev_requirements:
	$(PIP) install -r dev_requirements.txt
	sudo $(NPM) install -g grunt-cli
	# Need to be sudo for Travis
	sudo $(NPM) install
	$(GRUNT)
	test -e 'django_ode/settings/local.py' || echo 'from .base import *' > django_ode/settings/local.py

requirements:
	$(PIP) install -r requirements.txt

install:
	$(PYTHON) setup.py install
	$(PYTHON) manage.py syncdb --noinput

develop: requirements dev_requirements
	$(PYTHON) setup.py develop
	$(PYTHON) manage.py syncdb --noinput
	$(PYTHON) manage.py migrate accounts
	$(PYTHON) manage.py migrate frontend
	$(PYTHON) manage.py migrate flatblocks

production:
	# done in salt state
	# sudo $(NPM) install -g grunt-cli bower
	$(NPM) install
	$(NPM) install bower
	$(GRUNT)
	$(PYTHON) manage.py syncdb --noinput
	$(PYTHON) manage.py migrate accounts
	$(PYTHON) manage.py migrate frontend
	$(PYTHON) manage.py migrate flatblocks
	$(PYTHON) manage.py collectstatic --noinput
	$(PYTHON) manage.py compilemessages -l fr

schemamigration:
	$(PYTHON) manage.py schemamigration accounts --auto

migrate:
	$(PYTHON) manage.py migrate accounts

$(FLAKE8): virtualenv
	$(PIP) install flake8

test: flake8
	$(PYTHON) $(TEST_COMMAND)

coverage: flake8
	$(COVERAGE) run --branch --source=. --omit=$(OMIT) $(TEST_COMMAND)
	$(COVERAGE) report -m

start: $(PROC) .env
	$(PROC) start -f $(PROCFILE)

backup:
	#TODO

flake8: $(FLAKE8)
	flake8 --exclude=$(OMIT) .

serve:
	python manage.py runserver
