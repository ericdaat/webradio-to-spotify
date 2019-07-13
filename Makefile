#!make
SHELL=/bin/bash

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

export PYTHONPATH="."

init-db:
	PYTHONPATH="." python scripts/init_db.py

tests:
	python -m unittest discover -s tests;

docs:
	sphinx-apidoc ./src -o docs/source -M;
	cd docs && make clean && make html && cd ..;
	open docs/build/html/index.html;

start:
	uwsgi wsgi.ini

update-playlist:
	curl -X GET localhost:9999/api/update_playlist;
