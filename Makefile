.PHONY = test coverage

test:
	uv run pytest -v
coverage:
	uv run pytest --cov=src
