FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV DB_HOST=mysql
ENV DB_PASSWORD=Pa55w0rd
ENV POETRY_VERSION=2.1.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

RUN apt update \
    && apt install -y --no-install-recommends default-mysql-client libmariadb-dev libpq-dev \
    && apt install -y --no-install-recommends libcurl4-openssl-dev \
    && apt install -y --no-install-recommends build-essential \
    && apt install -y --no-install-recommends xmlsec1 \
    && apt install -y --no-install-recommends libxrender1 \
    && apt install -y --no-install-recommends libxext6 \
    && apt install -y --no-install-recommends libmagic1 \
    && apt install -y --no-install-recommends libssl-dev \
    && apt install -y --no-install-recommends wget \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r docker && useradd -r -m -g docker docker

WORKDIR /app/integrations
# Install poetry separated from system interpreter

RUN mkdir -p /home/docker/.cache/pypoetry

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY . /app/integrations

RUN poetry install

RUN chown -R docker:docker /home/docker

VOLUME /home/docker
RUN apt-get -y autoremove --purge && apt-get autoclean -y
RUN chown -R docker /opt
ENV PYTHONPATH $PYTHONPATH:/app
EXPOSE 8000
USER docker
CMD ["/app/integrations/entrypoint.sh"]
