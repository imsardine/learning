VENV_DIR = $(PWD)/venv
export TEST ?= tests/
export PYTHONDONTWRITEBYTECODE = 1
export TOX_TESTENV_PASSENV = PYTHONDONTWRITEBYTECODE

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install tox==3.1.2

test:
	PATH=$(VENV_DIR)/bin:$(PATH) tox

test-py2:
	PATH=$(VENV_DIR)/bin:$(PATH) tox -e py2

test-py3:
	PATH=$(VENV_DIR)/bin:$(PATH) tox -e py3
