FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 --retries 5 -r requirements.txt

COPY src/ ./src/
COPY data/clean/ ./data/clean/
COPY docker/backend-entrypoint.sh ./docker/backend-entrypoint.sh

EXPOSE 8000
CMD ["sh", "docker/backend-entrypoint.sh"]
