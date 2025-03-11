ARG BASE_IMAGE_TAG=3.11
FROM python:${BASE_IMAGE_TAG}

ARG WPM_VERSION_REQUIREMENT=latest
ARG PYPI_INDEX=https://pypi.org/simple
ARG TEST_PYPI_INDEX=https://test.pypi.org/simple

WORKDIR /wpm-root

COPY requirements.txt .

RUN pip install --index-url ${PYPI_INDEX} --no-cache-dir -r requirements.txt

RUN pip install --index-url ${TEST_PYPI_INDEX} --no-cache-dir wavelogpostmanager==${WPM_VERSION_REQUIREMENT}

RUN wpm -init

WORKDIR /wpm-root/wpm

CMD wpm -start

