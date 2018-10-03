MAKEFLAGS=--warn-undefined-variables

# Parameters
-include Makefile.credentials
-include Makefile.settings
TEST ?= tests/
TEST_ENVS ?=
TEST_MARK ?=
ENDPOINT ?= /apps?format=json

# Internal Variables
docker_image = learning-hockeyapp.local
docker_opts =
pytest_opts = -vvv -o log_cli=true
hockeyapp_api = https://rink.hockeyapp.net/api/2

docker_opts += --env HOCKEYAPP_APP_ID=$(HOCKEYAPP_APP_ID)
docker_opts += --env HOCKEYAPP_TOKEN=$(HOCKEYAPP_TOKEN)

ifneq ($(TEST_MARK),)
pytest_opts += -m '$(TEST_MARK)'
endif

define docker_run
	docker run --rm -it \
	  --volume $(PWD):/workspace \
	  --volume $(PWD)/tmp:/tmp \
	  $(docker_opts) \
	  $(docker_image) $(1)
endef

setup:
	docker build -t $(docker_image) .
	$(call docker_run,tox --notest)

shell: docker_opts += --volume ~/.vimrc:/root/.vimrc
shell:
	$(call docker_run,)

request:
	$(call docker_run,curl \
	  -H 'X-HockeyAppToken: $(HOCKEYAPP_TOKEN)' \
	  $(hockeyapp_api)$(ENDPOINT) | jq . \
	)

test: docker_opts += --env TEST=$(TEST)
test: docker_opts += --env TOXENV=$(TEST_ENVS)
test: docker_opts += --env TOX_TESTENV_PASSENV="HOCKEYAPP_APP_ID HOCKEYAPP_TOKEN"
test: docker_opts += --env PYTEST_OPTS="$(pytest_opts)"
test:
	$(call docker_run,tox)

clean:
	git clean -Xdf
