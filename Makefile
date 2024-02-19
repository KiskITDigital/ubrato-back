include .env

.PHONY: install installdev run format docker_build docker_run docker_clean migration_up migration_down

migration_up:
	migrate -path ./app/repositories/migration/ -database "postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable" -verbose up

migration_down:
	migrate -path ./app/repositories/migration/ -database "postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable" -verbose down

docker_build:
	docker build --build-arg GIT_VERSION=$(git describe --long --tags --always) -t ubrato:0.1.0 .

docker_run:
	docker run --name ubrato -e SERVER_PORT=$(SERVER_PORT) -e SERVER_ADDR=$(SERVER_ADDR) -p $(SERVER_PORT):8080 ubrato:0.1.0

docker_clean:
	docker stop ubrato
	docker rm ubrato
	docker rmi ubrato:0.1.0

install:
	poetry install

installdev:
	poetry install --with dev

run:
	cd app && uvicorn main:app --host $(SERVER_ADDR) --port $(SERVER_PORT)

format:
	black ./app --line-length 79
	flake8 ./app