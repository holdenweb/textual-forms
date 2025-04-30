.PHONY = test coverage release

test:
	uv run pytest -v
coverage:
	uv run pytest --cov=
release:
	uv run python src/release.py $(version)
