FROM python:3.10-alpine

RUN apk add --no-cache \
    jq \
    qt6-qtdeclarative-dev
ENV PATH=${PATH}:/usr/lib/qt6/bin/

WORKDIR /tmp/pip-install
COPY requirements.txt .
RUN pip install --no-cache-dir --user \
    -r requirements.txt \
    mypy-gitlab-code-quality \
    pylint-gitlab \
    && pip cache purge \
    && rm -rf ./*
