.PHONY: docs
init:
	pip install pipenv --upgrade
	pipenv install --dev --skip-lock

test:
	pipenv run py.test tests

ci:
	pipenv run py.test -n 8 --boxed --junitxml=report.xml

test-readme:
	@pipenv run python setup.py check --restructuredtext --strict && ([ $$? -eq 0 ] && echo "README.rst ok") || echo "Invalid markup in README.rst!"
