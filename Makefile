run_in_docker:
	docker-compose build
	MONGO_INITDB_ROOT_USERNAME=hiddenuser MONGO_INITDB_ROOT_PASSWORD=hiddenpass docker-compose up -d
