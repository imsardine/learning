MAKEFLAGS=--warn-undefined-variables

# Parameters
# MYSQL
TEST ?= tests/
TEST_ENVS ?=
ifdef MYSQL
TEST_MARK ?=
else
TEST_MARK ?= not mysql
endif

# Internal Variables
docker_image = learning-sqlalchemy.local
docker_opts =
pytest_opts =

ifneq ($(TEST_MARK),)
pytest_opts += -m '$(TEST_MARK)'
endif

ifdef MYSQL
mysql_container = mysql-learning-sqlalchemy
mysql_version = 5.7.23
mysql_db = db
mysql_user = user
mysql_password = secret

docker_opts += --link $(mysql_container):mysql
docker_opts += --env MYSQL_DB=$(mysql_db)
docker_opts += --env MYSQL_USER=$(mysql_user)
docker_opts += --env MYSQL_PASSWORD=$(mysql_password)

TEST_MARK =

define docker_run_mysql
	@docker rm -f $(mysql_container) 2>&1 || true
	docker run --rm -d --name $(mysql_container) \
	  --env MYSQL_DATABASE=$(mysql_db) \
	  --env MYSQL_USER=$(mysql_user) \
	  --env MYSQL_PASSWORD=$(mysql_password) \
	  --env MYSQL_ROOT_PASSWORD=admin \
	  mysql:$(mysql_version)
	until docker logs $(mysql_container) 2>&1 \
	  | grep 'MySQL init process done. Ready for start up.'; \
	  do continue; done
	@echo 'To connect to MySQL server, run: mysql -h mysql -u user -psecret db'
endef
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
	docker pull mysql:$(mysql_version)
	$(call docker_run,tox --notest)

shell:
ifdef MYSQL
	$(call docker_run_mysql)
endif
	$(call docker_run,)

test: docker_opts += --env TEST=$(TEST)
test: docker_opts += --env TOXENV=$(TEST_ENVS)
test: docker_opts += --env TOX_TESTENV_PASSENV="MYSQL_DB MYSQL_USER MYSQL_PASSWORD"
test: docker_opts += --env PYTEST_OPTS="$(pytest_opts)"
test:
ifdef MYSQL
	$(call docker_run_mysql)
	$(call docker_run,tox) || true
#	docker stop $(mysql_container)
else
	$(call docker_run,tox)
endif

clean:
	git clean -Xdf
	docker rm -f $(mysql_container) || true
