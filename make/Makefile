TEST ?= tests/
VENV_DIR = $(PWD)/venv

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

test:
	$(VENV_DIR)/bin/pytest -vvv $(TEST)
