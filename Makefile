.PHONY: clean-pyc clean-build docs clean upgrade requirements lint test test-all coverage dist

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "requirements - install development environment requirements"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "dist - package"
	@echo "upgrade update the python requirements files to use the latest releases satisfying our constraints"

clean: clean-build clean-pyc
	rm -fr htmlcov/

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

requirements: ## install development environment requirements
	uv sync --group dev

lint:
	flake8 src tests

test:
	python -Wd -m pytest tests/

test-all:
	tox

coverage:
	coverage run --source src/enmerkar_underscore -m pytest tests/
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	$(MAKE) -e -C docs clean
	$(MAKE) -e -C docs html

dist: clean
	uv build
	ls -l dist

upgrade: ## update python dependencies
	uv run --with edx-lint edx_lint write_uv_constraints pyproject.toml
	uv lock --upgrade
