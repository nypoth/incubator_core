FROM python:3.9
WORKDIR /opt/incubatore/core
COPY Pipfile .
RUN pip install pipenv && apt update && apt install nano
RUN pipenv install --system --skip-lock
COPY . .

CMD gunicorn -c gunicorn_config.py wsgi:application