FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

WORKDIR /app
COPY app/requirements.txt .

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=20 -r requirements.txt
COPY ./app .
CMD ["./wait-for-it.sh", "python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
