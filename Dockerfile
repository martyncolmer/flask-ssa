FROM python:3.6-alpine

RUN mkdir -p /deploy/flaskapp
WORKDIR /deploy/flaskapp

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY flask_ssa flask_ssa
COPY instance instance
COPY gunicorn_config.py gunicorn_config.py

ENV FLASK_APP flask_ssa

EXPOSE 5000

ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "/deploy/flaskapp/gunicorn_config.py", "flask_ssa:create_app()"]