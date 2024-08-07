FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    pkg-config \
    default-mysql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /nginx/daphne

WORKDIR /app/project

# RUN python manage.py collectstatic --noinput

CMD ["bash", "-c", "rm -f /app/nginx/daphne/daphne.sock && daphne -u /app/nginx/daphne/daphne.sock project.asgi:application"]
