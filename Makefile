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
