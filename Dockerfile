FROM python:3.12-slim
WORKDIR /opt/app
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY run_uwsgi.sh run_uwsgi.sh
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN pip install --upgrade pip  \
    && pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uwsgi", "--strict", "--ini", "uwsgi.ini"]