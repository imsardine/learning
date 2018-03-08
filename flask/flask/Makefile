run:
	$(call flask,run)

shell:
	$(call flask,shell)

test:
	pytest --verbose -vv tests

define flask
	FLASK_APP=run python -m flask $(1)
endef

