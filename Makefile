.PHONY: tests
tests:
	@poetry run pytest -sv tests

.PHONY: dist
dist:
	@rm -rf dist/
	@rm -rf build/
	@poetry build

.PHONY: publish
publish:
	@poetry publish

.PHONY: coverage
coverage:
	@poetry run pytest --cov=hapless tests

.PHONY: install
install:
	@poetry install --with dev --all-extras

.PHONY: isort
isort:
	@poetry run isort .

.PHONY: black
black:
	@poetry run black .

.PHONY: lint
lint:
	@poetry run flake8 .

.PHONY: changelog
changelog:
	@poetry run semantic-release changelog --unreleased

.PHONY: print-next-version
print-next-version:
	@poetry run semantic-release print-version --next
