FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install pipenv

WORKDIR /app

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

COPY ./app .

CMD ["python", "manage.py", "runserver", "8000"]
