TEST ?= tests/

docker_image = learning-jquery.local
docker_opts = --env NODE_PATH=/workspace/node_modules

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
	$(call docker_run,npm install puppeteer@1.8.0)

shell:
	$(call docker_run)

test:
	$(call docker_run,tox)

