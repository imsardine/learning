include Makefile.settings

TEST ?= tests/
VENV_DIR = $(PWD)/venv
ENDPOINT ?= /projects

setup:
	virtualenv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

test:
	@PATH=$(VENV_DIR)/bin:$(PATH) \
	GITLAB_URL=$(GITLAB_URL) \
	GITLAB_ACCESS_TOKEN=$(GITLAB_ACCESS_TOKEN) \
		pytest -vvv $(TEST)

request:
	@curl \
		-H 'Private-Token: $(GITLAB_ACCESS_TOKEN)' \
		--dump-header /dev/stderr \
		'$(GITLAB_URL)$(ENDPOINT)' | jq -r .

