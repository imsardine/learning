run:
	$(call flask,run)

shell:
	$(call flask,shell)

test:
	pytest

define flask
	FLASK_APP=run python -m flask $(1)
endef

