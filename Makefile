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
