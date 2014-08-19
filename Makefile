# Some simple testing tasks (sorry, UNIX only).


pep8:
	pep8 .

flake:
	pyflakes .

test: flake pep8
	nosetests -s tests

vtest: flake pep8
	nosetests -s -v tests

testloop:
	while sleep 1; do nosetests -s tests ; done

cov cover coverage: flake pep8
	nosetests -s --with-coverage --cover-html --cover-package aioes --cover-branches --cover-erase
	echo "open file://`pwd`/cover/index.html"

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
	cd docs && make html
	echo "open file://`pwd`/docs/_build/html/index.html"

.PHONY: all build venv flake test vtest testloop cov clean doc
