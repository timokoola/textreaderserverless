.PHONY: help clean clean-pyc clean-build list test test-all coverage docs init init_with_pyenv deploy upload_lambda package_lambda

init:
	touch ~/textreader_env.sh && . ~/textreader_env.sh && ./virtualenv_creator.sh && source ~/virtualenvs/textreader/bin/activate

init_with_pyenv:
	./virtualenv_creator_jenkins_pyenv.sh && ./virtualenv_mini_creator_pyenv.sh

activate:
	source ~/virtualenvs/textreader/bin/activate

miniactivate:
	source ~/virtualenvs/textreader_mini/bin/activate

help:
	@echo "init - initialize virtualenvs, import environment variables"
	@echo "init_with_pyenv - create virtualenvs using PyEnv"
	@echo "activate - activate development virtualenv"
	@echo "miniactivate - activate virtualenv for AWS Lambda deployment"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "deploy - package and upload code to AWS lambda function"
	@echo "upload_lambda - upload code to AWS lambda function"
	@echo "package_lambda - package code and packages in mini virtualenv for upload in AWS Lambda"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 textreader test

typecheck:
	mypy spinnershop --ignore-missing-imports

test:
	python setup.py install && python -m pytest --ff

coverage:
	coverage run --source textreader setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/textreader.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ textreader
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

deploy:
	package_lambda upload_lambda

upload_lambda:
	aws lambda update-function-code --function-name textreaderdemo --zip-file fileb://deploy_lambda.zip --region eu-west-1

package_lambda:
	./package_lambda.sh


