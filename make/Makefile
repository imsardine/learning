VENV = venv-make

test:
	$(VENV)/bin/pytest -vvv

setup:
	virtualenv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt