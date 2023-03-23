project-name=python-graylog
user=$(shell whoami)


env-create:
	conda update -y -n base -c defaults conda
	conda create -y -n ${project-name} python=3.10
	# conda activate ${project-name}
	# pip install --upgrade pip
	# conda env update --file environment.yml


env-export:
	conda env export --no-builds | sed "/libcxx/d" | sed -e '/- pip:/i\'$$'\n  - pip' > environment.yml
	pip list --format=freeze > requirements.txt


env-update:
	conda env update --file environment.yml

.PHONY: clean-pyc clean-build test

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

release: sdist
	twine check dist/*
	twine upload dist/*

release-test: sdist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

sdist: clean
	python setup.py sdist bdist_wheel
	ls -l dist

test:
	pip install -e .
	flake8 .
	py.test tests/

coverage:
	coverage run --source=dotenv --omit='*tests*' -m py.test tests/ -v --tb=native
	coverage report

coverage-html: coverage
	coverage html
