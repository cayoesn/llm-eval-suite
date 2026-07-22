FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

COPY pyproject.toml .
RUN pip install --no-cache-dir .[dev]

COPY app/ ./app/
COPY tests/ ./tests/

CMD ["pytest", "--cov=app", "--cov-report=term-missing"]
