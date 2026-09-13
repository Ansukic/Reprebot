# Contribuir a Reprebot

Gracias por el interés. Este documento explica el flujo de trabajo.

## Flujo de cambios

1. Haz fork del repositorio (o crea una rama si tienes acceso directo)
2. Crea una rama desde `main` con nombre descriptivo:
   ```
   git checkout -b feat/whatsapp-webhook
   git checkout -b fix/chat-response-schema
   ```
3. Haz tus cambios con commits pequeños y claros
4. Abre un Pull Request hacia `main` describiendo qué hace y por qué
5. Espera revisión de alguien del CEIS antes del merge

Nunca hagas push directo a `main`.

## Convenciones

### Ramas

- `feat/` — nueva funcionalidad
- `fix/` — corrección de bug
- `docs/` — solo documentación
- `chore/` — tooling, configuración, dependencias

### Commits

Escribe commits en español o inglés, pero consistentes. Ejemplo:

```
agrega validación de firma en webhook de whatsapp
```

### Backend (Python)

- Seguimos PEP 8. La herramienta de referencia es `ruff` — si pasa `ruff check`, está bien
- Archivos y funciones en snake_case, clases en PascalCase, constantes en UPPER_CASE
- La lógica va en `app/services/`, los endpoints en `app/api/` solo exponen rutas y validan entrada

## Setup del backend

```bash
cd apps/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La documentación interactiva queda en http://127.0.0.1:8000/docs

## Reportar bugs

Abre un issue con:
- Qué pasó y qué esperabas
- Pasos para reproducir
- Versión de Python y sistema operativo
