# syntax=docker/dockerfile:1.2

ARG RUNTIME_VERSION="3.10"
ARG DISTRO_VERSION="slim-buster"

FROM python:${RUNTIME_VERSION}-${DISTRO_VERSION}

ARG SOURCE_DIR="/pritunl-api"
ARG TOML_CLI_VERSION="0.2.3"

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install curl jq -y

RUN curl -L -o /tmp/toml-${TOML_CLI_VERSION}-x86_64-linux.tar.gz https://github.com/gnprice/toml-cli/releases/download/v${TOML_CLI_VERSION}/toml-${TOML_CLI_VERSION}-x86_64-linux.tar.gz \
    && tar -xzf /tmp/toml-${TOML_CLI_VERSION}-x86_64-linux.tar.gz -C /tmp \
    && cp /tmp/toml-${TOML_CLI_VERSION}-x86_64-linux/toml /usr/local/bin/ \
    && rm -Rf /tmp/toml-${TOML_CLI_VERSION}-x86_64-linux

RUN mkdir -p ${SOURCE_DIR}
WORKDIR ${SOURCE_DIR}
COPY . ${SOURCE_DIR}

RUN python -m pip install --upgrade pip
RUN pip install -e .
RUN toml get pyproject.toml project.optional-dependencies.repl | jq -r '.[]' | xargs pip install

CMD [ "ptipython" ]
