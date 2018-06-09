TEST ?= tests/
VENV_DIR = $(PWD)/venv

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

test:
	PATH=$(VENV_DIR)/bin:$(PATH) pytest -vvv \
		--ignore=tests/data/tests/ $(TEST)
