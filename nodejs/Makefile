TEST ?= tests/
VENV_DIR = $(PWD)/venv

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install tox==3.1.2

test:
	PATH=$(VENV_DIR)/bin:$(PATH) tox
