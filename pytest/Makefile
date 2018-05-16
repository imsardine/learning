TEST ?= tests/
VENV_DIR = $(PWD)/venv-pytest

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

test:
	PATH=$(VENV_DIR)/bin:$(PATH) pytest -vvv $(TEST)
