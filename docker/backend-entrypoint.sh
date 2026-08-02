#!/bin/sh
set -e

echo "Esperando a Qdrant..."
until python -c "import os, urllib.request; urllib.request.urlopen(os.environ.get('QDRANT_URL', 'http://qdrant:6333') + '/readyz')" 2>/dev/null; do
  sleep 2
done

echo "Indexando contenido..."
python -m src.ingestion.indexer

echo "Arrancando API..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000
