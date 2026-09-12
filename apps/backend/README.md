# ¡Bienvenido al Backend!

API de Reprebot construida con FastAPI.

## Requisitos

- Python 3.11 o superior

## Cómo iniciar

Desde esta carpeta (`apps/backend`):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
fastapi dev
```

Importante: `fastapi dev` debe ejecutarse desde `apps/backend/`, porque los imports son relativos a la carpeta `app/`.

Si todo funciona, la documentación interactiva está en http://127.0.0.1:8000/docs o http://127.0.0.1:8000/redoc

## Estructura del proyecto

```
apps/backend
├── app/
│   ├── api/          # endpoints: solo exponen rutas y validan entrada
│   │   ├── chat.py
│   │   ├── health.py
│   │   └── whatsapp.py
│   ├── models/       # esquemas de datos (Pydantic)
│   │   └── chat_message.py
│   ├── services/     # lógica de negocio
│   │   └── chat_service.py
│   └── main.py       # entry point
├── requirements.txt
└── README.md
```

## Convenciones de código

Seguimos PEP 8, verificado con `ruff`:

- Archivos y funciones: `snake_case` (`chat_service.py`, `answer_message()`)
- Clases: `PascalCase` (`ChatMessage`, `ChatResponse`)
- Constantes: `UPPER_CASE` (`API_URL`, `TIMEOUT_SECONDS`)

## Notas de diseño

- `api/` no contiene lógica de negocio: solo rutas y validación. La lógica va en `services/`
- `models/` contiene los esquemas Pydantic que comparten api y services
- `chat_service.answer` es un echo por ahora; falta la conexión con el modelo de IA (ver TODO en el código)
