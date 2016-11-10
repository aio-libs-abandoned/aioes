# Some simple testing tasks (sorry, UNIX only).


pep8:
	pep8 .

flake:
	pyflakes .

test: flake pep8
	pytest tests

vtest: flake pep8
	pytest -v tests


cov cover coverage: flake pep8
	pytest --cov=aioes tests
	@echo "open file://`pwd`/coverage/index.html"

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

.PHONY: all build venv flake test vtest testloop cov clean doc
