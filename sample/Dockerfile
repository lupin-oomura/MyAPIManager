FROM python:3.10-slim

WORKDIR /app
COPY . /app

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# GunicornとEventletをインストール
RUN pip install gunicorn eventlet

EXPOSE 8080
CMD ["gunicorn", "--worker-class", "eventlet", "--bind", "0.0.0.0:8080", "app:app"]
