# Some simple testing tasks (sorry, UNIX only).

TEST_ARGS ?= -v

flake:
	flake8 .

test: flake
	py.test tests $(TEST_ARGS)

vtest: flake
	py.test -v tests


cov cover coverage: flake
	py.test --cov tests $(TEST_ARGS)
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf cover
	rm -rf build

doc:
	@make html -C docs
	@echo "open file://`pwd`/docs/_build/html/index.html"

setup-check:
	python setup.py check -rms

cmp:
	python cmp.py

.PHONY: all build venv flake test vtest testloop cov clean doc
