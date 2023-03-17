# syntax=docker/dockerfile:1.2

ARG RUNTIME_VERSION="3.10"
ARG DISTRO_VERSION="slim-buster"
ARG SOURCE_DIR="/pritunl-api"

FROM python:${RUNTIME_VERSION}-${DISTRO_VERSION}

ARG SOURCE_DIR

RUN apt-get update && \
    apt-get upgrade -y

RUN mkdir -p ${SOURCE_DIR}
WORKDIR ${SOURCE_DIR}

COPY . ${SOURCE_DIR}

RUN python -m pip install --upgrade pip

CMD [ "ptipython" ]
