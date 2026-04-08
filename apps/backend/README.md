#  ¡Bienvenido al Backend!
¡Hola!

Esta es la sección del proyecto encargada del backend, para esto utilizamos fastapi, un framework de python que permite hacer backend bueno, bonito y rápido.


¡Te recomendamos leer estas secciones antes de hacer cambios sobre el repositorio!


  ## Algunas notas sobre código "decente"
  Antes de hablar sobre la distribución del proyecto, queremos hablar de algunas formas de nombrar cosas útiles del PEP 8(la guía de estilos de python https://peps.python.org/pep-0008/).

## Para los archivos

Usa snake_case
```
chat_service.py
chat_message.py
whatsapp_service.py
```
Evita:
```
chatService.py
ChatService.py
chat-service.py
```
## Classes

Usa PascalCase
```
class ChatMessage:
class ChatResponse:
class WhatsAppMessage:
```

## Funciones

Usa snake_case
```
def answer_message():
def send_whatsapp_message():
```

## Variables

Usa snake_case
```
user_message = "hello"
ai_response = "hi"
```
## Constantes

Usa UPPER_CASE
```
API_URL = "http://..."
TIMEOUT_SECONDS = 30
```
  
  

##  ¿Cómo Iniciar el proyecto?

Recomendamos inicializar un entorno virtual, para que no haya conflictos en el momento de instalar las dependencias, visita https://stackoverflow.com/questions/43069780/how-can-i-create-a-virtual-environment-with-python-3 para más información.

Luego, dentro del (venv) ejecuta:

    pip install -r /path/to/requirements.txt

Finalmente, para iniciar el backend:

    fastapi dev

Y si todo está funcionando correctamente, verás que fastapi está ejecutandose, puedes ir a la documentación en http://127.0.0.1:8000/docs#/ o http://127.0.0.1:8000/redoc

¡Visita https://fastapi.tiangolo.com para la documentación completa!

##  Estructura del proyecto

  

- **apps/backend**
  - **app/**
    - **api/** *(routes / endpoints)*
      - chat.py
      - whatsapp.py
      - health.py
    - **services/** *(business logic of each service)*
      - chat_service.py
      - ai_client.py
      - whatsapp_service.py
    - **core/** *(configuration and core settings)*
      - config.py
    - **models/** *(data structures and schemas)*
      - schemas.py
    - main.py *(application entry point)*
  - requirements.txt
  - README.md
  
  

##  Breve explicación

  

###  apps/backend

  

Es la carpeta que contiene todo el proyecto del back, aquí tenemos el Readme, requirements.txt y la carpeta de la aplicación.

  

###  apps/backend/app

  

En esta carpeta tenemos todo el código "real" del backend.

  
  

###  apps/backend/app/api

  

Esta es la carpeta que contiene el router, aquí nos encargamos de exponer las rutas o endpoints, SOLO MOSTRAMOS LAS RUTAS Y VÁLIDAMOS ALGUNAS COSAS, la lógica de lo que hace la ruta, se hace en la carpeta services.
  

###  apps/backend/app/core

Aquí almacenamos configuraciones del env o el logger (si se hace)

  

###  apps/backend/app/models

Esta es la carpeta que continen los modelos de datos que usamos en los servicios o en la api. Por ejemplo, aquí modelamos los mensajes

  

###  apps/backend/app/services

  

Esta es la carpeta que contiene la lógica real de cada una de las cosas que hacemos, puede que un solo servicio sea usado por varios endpoints para realizar alguna acción.


