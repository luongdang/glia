FROM python:3.9.15-alpine3.16

WORKDIR /code

# COPY requirements.txt /code
# RUN pip install -r requirements.txt
RUN apk add --no-cache curl gcc libressl-dev musl-dev libffi-dev
RUN pip install poetry
RUN apk del curl gcc libressl-dev musl-dev libffi-dev

COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false && poetry install 

COPY ./app /code/app
CMD uvicorn app.main:app --host 0.0.0.0

