FROM python:3.10-slim-buster AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip \
    && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile


FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]