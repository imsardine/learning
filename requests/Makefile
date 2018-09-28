MAKEFLAGS=--warn-undefined-variables

# Parameters
TEST ?= tests/
TEST_ENVS ?=

# Internal Variables
docker_image = learning-requests.local
docker_opts =

httpbin_image = kennethreitz/httpbin
httpbin_container = httpbin-learning-requests

define docker_run
	docker run --rm -it \
	  --volume $(PWD):/workspace \
	  --volume $(PWD)/tmp:/tmp \
	  --link $(httpbin_container):httpbin \
	  $(docker_opts) \
	  $(docker_image) $(1)
endef

define docker_run_httpbin
	@docker rm -f $(httpbin_container) 2>&1 || true
	docker run --rm -detach --name $(httpbin_container) \
	  $(httpbin_image)
endef

setup:
	docker build -t $(docker_image) .
	docker pull $(httpbin_image)
	$(call docker_run,tox --notest)

shell:
	$(call docker_run_httpbin)
	$(call docker_run,bash)
	docker stop $(httpbin_container)

test: docker_opts += --env TEST=$(TEST)
test: docker_opts += --env TOXENV=$(TEST_ENVS)
test:
	$(call docker_run_httpbin)
	$(call docker_run,tox)
	docker stop $(httpbin_container)

clean:
	git clean -Xdf
