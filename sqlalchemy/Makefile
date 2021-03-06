MAKEFLAGS=--warn-undefined-variables

# Parameters
-include credentials.mk
-include settings.mk
TEST ?= tests/
TEST_ENVS ?=
TEST_MARK ?=

# Internal Variables
docker_opts =
pytest_opts = -vvv

ifneq ($(TEST_MARK),)
  pytest_opts += -m '$(TEST_MARK)'
endif

define docker_run
	docker-compose run --rm \
	  $(docker_opts) \
	  dev $(1)
endef

setup:
	docker-compose build --no-cache

up:
	docker-compose up --detach
	until docker-compose logs mysql 2>&1 | grep 'mysqld: ready for connections'; do continue; done

down:
	docker-compose down

shell: docker_opts += --volume ~/.vimrc:/root/.vimrc
shell:
	$(call docker_run,)

test: docker_opts += -e TEST=$(TEST)
test: docker_opts += -e TOXENV=$(TEST_ENVS)
test: docker_opts += -e PYTEST_OPTS="$(pytest_opts)"
test:
	$(call docker_run,tox)

clean:
	docker-compose down --rmi local --volumes
	git clean -Xdf
