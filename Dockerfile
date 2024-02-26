FROM python:3.11.6-alpine3.18

ARG SERVER_PORT=3000
ARG SERVER_ADDR=0.0.0.0
ARG GIT_VERSION

ENV SERVER_PORT=${SERVER_PORT}
ENV SERVER_ADDR=${SERVER_ADDR}
ENV GIT_VERSION=${GIT_VERSION}

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100


RUN pip install poetry

WORKDIR /ubrato
COPY poetry.lock pyproject.toml /ubrato/

COPY .env /ubrato
COPY ./app /ubrato/app
COPY ./scripts /ubrato/scripts

RUN poetry lock

RUN poetry install

EXPOSE $SERVER_PORT

HEALTHCHECK --interval=60s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:${SERVER_PORT}/health/ || exit 1

ENTRYPOINT [ "sh", "./scripts/run.sh" ]