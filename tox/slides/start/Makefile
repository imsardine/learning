venv_dir = $(PWD)/venv
export TEST ?= tests/

setup:
	virtualenv $(venv_dir)
	$(venv_dir)/bin/pip install tox==3.0.0

test:
	PATH=$(venv_dir)/bin:$(PATH) tox

test-py2:
	PATH=$(venv_dir)/bin:$(PATH) tox -e py27

test-py3:
	PATH=$(venv_dir)/bin:$(PATH) tox -e py36
