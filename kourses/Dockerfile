FROM python:3.12

WORKDIR /code

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        gcc \
        musl-dev \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

ENV SECRET_KEY=&SECRET_KEY
ENV CELERY_BROKER_URL=&CELERY_BROKER_UR
ENV CELERY_RESULT_BACKEND=&CELERY_RESULT_BACKEND

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
