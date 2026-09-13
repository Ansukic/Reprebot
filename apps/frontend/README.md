# Frontend de prueba

Interfaz estática para probar Reprebot antes de integrarlo en el foro.

No necesita Node ni build:

- `index.html` — chat y vista de documentos
- `styles.css` — tema oscuro con acento UNAL
- `app.js` — llamadas a `/api/chat`, `/api/search`, `/api/documents` y `/api/health`

El backend sirve esta carpeta en `/`. Arranque el servidor desde `apps/backend` y abra http://127.0.0.1:8000/.
