#!make
SHELL=/bin/bash

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

export PYTHONPATH="."

tests:
	python -m unittest discover -s tests;
