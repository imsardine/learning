include Makefile.settings

TEST ?= tests/
VENV_DIR = $(PWD)/venv

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

test:
	@PATH=$(VENV_DIR)/bin:$(PATH) \
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) \
	AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) \
	S3_BUCKET=$(S3_BUCKET) \
		pytest -vvv $(TEST)

