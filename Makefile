include .env
include ./proto/proto.mk

PROTO_PATH = ./proto
PROTO_OUT = ./app/schemas/pb

.PHONY: install installdev run format docker_build docker_run docker_clean migration_up migration_down

migration_up:
	migrate -path ./app/repositories/postgres/migration/ -database "postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable" -verbose up
	cd ./app/repositories/typesense/migration && TYPESENSE_HOST=$(TYPESENSE_HOST) TYPESENSE_API_KEY=$(TYPESENSE_API_KEY) ./migration.sh

migration_down:
	migrate -path ./app/repositories/postgres/migration/ -database "postgresql://postgres:12345@localhost:5432/postgres?sslmode=disable" -verbose down

docker_build:
	docker build --build-arg GIT_VERSION=$(git describe --long --tags --always) -t ubrato:0.1.0 .

docker_run:
	docker run --name ubrato -p $(SERVER_PORT):8080 \
	-e TYPESENSE_API_KEY=$(TYPESENSE_API_KEY) \
	-e TYPESENSE_HOST=$(TYPESENSE_HOST) -e TYPESENSE_PORT=$(TYPESENSE_PORT) \
	-e TYPESENSE_PROTOCOL=$(TYPESENSE_PROTOCOL) -e SERVER_PORT=8080 -e DB_DSN=$(DB_DSN) \
	-e JWT_SECRET=$(JWT_SECRET) -e JWT_TTL=$(JWT_TTL) -e SESSION_TTL=$(SESSION_TTL) \
	-e REDIS_HOST=$(REDIS_HOST) -e REDIS_PASSWORD=$(REDIS_PASSWORD) \
	-e NATS_HOST=$(NATS_HOST) -e DADATA_TOKEN=$(DADATA_TOKEN) \
	ubrato:0.1.0 --port=$(SERVER_PORT) --host=$(SERVER_ADDR)

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
	isort ./app --profile black
	black ./app --line-length 79
	flake8 ./app
