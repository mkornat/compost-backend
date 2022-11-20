FROM python:3.10-slim

COPY requirements.txt /requirements.txt

RUN pip install pip-tools && \
    pip pip-sync
