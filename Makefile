setup_virtualenv:
	virtualenv env -p $$(which python3)

install_requirements:
	./env/bin/pip install -r requirements.txt

run:
	./env/bin/python -m sd_eshop

run_from_scratch:
	$(MAKE) setup_virtualenv
	$(MAKE) install_requirements
	$(MAKE) run

test:
	./env/bin/python -m unittest

run_in_docker:
	docker-compose build
	MONGO_INITDB_ROOT_USERNAME=hiddenuser MONGO_INITDB_ROOT_PASSWORD=hiddenpass docker-compose up -d
