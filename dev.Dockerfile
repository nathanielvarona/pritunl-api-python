# syntax=docker/dockerfile:1.2

ARG RUNTIME_VERSION="3.10"
ARG DISTRO_VERSION="slim-buster"

FROM python:${RUNTIME_VERSION}-${DISTRO_VERSION}

ARG SOURCE_DIR="/pritunl-api"

RUN mkdir -p ${SOURCE_DIR}
WORKDIR ${SOURCE_DIR}
COPY . ${SOURCE_DIR}

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install curl -y

RUN python -m pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH:"
RUN poetry completions bash >> ~/.bash_completion

RUN poetry install --no-root --extras=repl

ENV SHELL=/bin/bash
CMD [ "bash" ]
