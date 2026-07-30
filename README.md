# RAG BBVA Asistente

Asistente conversacional (RAG) que responde preguntas sobre el contenido de un sitio web bancario. Extrae el contenido mediante web scraping, lo vectoriza e indexa, y genera respuestas con memoria de conversación por sesión.

> Proyecto en construcción. El README se completa a medida que avanzan las fases (ver estado abajo).

## Arquitectura

Diseño desacoplado: la interfaz (API/UI) llama a un núcleo RAG independiente del framework, con proveedores de LLM, embeddings y vector store intercambiables.

```
UI ──HTTP──► API (FastAPI) ──► Núcleo RAG ──► [Embeddings · Vector store · LLM · Historial]
```

## Stack

- Python 3.11
- FastAPI (API)
- Qdrant (base de datos vectorial)
- sentence-transformers (embeddings multilingües)
- Ollama (LLM local; proveedor intercambiable)
- SQLite (historial de conversación)
- Docker / docker-compose

## Requisitos previos

- Docker y Docker Compose
- (Opcional, para desarrollo) Python 3.11+

## Puesta en marcha

```bash
cp .env.example .env
docker compose up -d
```

- API: http://localhost:8000/health
- Qdrant: http://localhost:6333/dashboard

> El primer arranque descarga el modelo de Ollama. Las instrucciones completas de uso se documentan al cerrar las fases.

## Estado

- [x] Estructura, configuración y esqueleto Docker
- [ ] Web scraping (crudo + limpio)
- [ ] Indexado vectorial
- [ ] Núcleo RAG + memoria de conversación
- [ ] API + interfaz conversacional
- [ ] Analítica del historial
- [ ] README completo (patrones de diseño, decisiones, mejoras)
