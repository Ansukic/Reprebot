# Backend de Reprebot

Microservicio FastAPI para consultar documentos de la Universidad Nacional de Colombia con RAG.

## Requisitos

- Python 3.11 o superior
- Una API key de Groq

## Configuración

```bash
cd apps/backend
cp .env.example .env
```

Edite `.env`:

```env
GROQ_API_KEY=su-key
GROQ_CHAT_MODEL=openai/gpt-oss-120b
EMBEDDINGS_MODEL=jinaai/jina-embeddings-v2-base-es
CORS_ORIGINS=*
ADMIN_TOKEN=
```

La key real vive solo en `.env`. Ese archivo está ignorado por Git. `fastembed` descarga el modelo de embeddings localmente en la primera ingesta.

## Ejecutar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Ejecute los comandos desde `apps/backend/`. La interfaz de prueba queda en http://127.0.0.1:8000/ y la documentación en http://127.0.0.1:8000/docs.

## API

| Método | Ruta | Uso |
| --- | --- | --- |
| `GET` | `/api/health` | Estado, modelo y conteo de documentos/chunks |
| `POST` | `/api/chat` | Pregunta RAG; devuelve respuesta y fuentes |
| `POST` | `/api/search` | Recupera fuentes sin llamar al LLM |
| `POST` | `/api/documents` | Ingresa un PDF, TXT o MD mediante `multipart/form-data` |
| `GET` | `/api/documents` | Lista documentos indexados |
| `DELETE` | `/api/documents/{id}` | Borra un documento y sus chunks |

Ejemplo:

```bash
curl -F 'file=@reglamento.pdf' http://127.0.0.1:8000/api/documents

curl -X POST http://127.0.0.1:8000/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"¿Qué dice el reglamento sobre la representación estudiantil?"}'
```

Si `ADMIN_TOKEN` tiene valor, las operaciones de ingesta y borrado requieren `X-Admin-Token`. La autenticación queda desactivada cuando está vacío, útil para desarrollo local. Para integrar el foro, configure `CORS_ORIGINS` con sus orígenes reales y active el token.

## Estructura

```text
app/
├── api/
│   ├── chat.py
│   ├── documents.py
│   ├── health.py
│   └── search.py
├── core/config.py
├── models/chat_message.py
├── services/
│   ├── ai_client.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── ingest.py
│   ├── rag.py
│   └── store.py
└── main.py
```

El índice numpy y sus metadatos se guardan en `data/`, que no se versiona.
