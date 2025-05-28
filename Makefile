.PHONY = test coverage release

test:
	uv run pytest -v
coverage:
	uv run pytest --cov src/textual_forms
release:
ifneq   "$(version)" ""
	uv run python src/release.py $(version)
else
	@grep 'version =' pyproject.toml
endif

