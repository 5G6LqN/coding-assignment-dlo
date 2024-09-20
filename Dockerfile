FROM python:3.12-slim-bookworm
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED=1
COPY requirements.in /app/requirements.txt
WORKDIR /app

RUN pip --no-cache-dir install pip-tools && \
    pip-sync --pip-args "--no-cache-dir"
