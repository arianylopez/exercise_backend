FROM python:3.12-slim

RUN groupadd -r web && useradd -r -g web web
WORKDIR /opt/app
ENV DJANGO_SETTINGS_MODULE='config.settings'

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

COPY --chown=web:web . .
USER web
EXPOSE 8000

ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi/uwsgi.ini"]