#  ¡Bienvenido al Backend!

  

##  ¿Cómo Iniciar el proyecto?

Recomendamos inicializar un entorno virtual, para que no haya conflictos en el momento de instalar las dependencias, visita https://stackoverflow.com/questions/43069780/how-can-i-create-a-virtual-environment-with-python-3 para más información.

Luego, dentro del (venv) ejecuta:

    pip install -r /path/to/requirements.txt

Finalmente, para iniciar el backend:

    fastapi dev

Y si todo está funcionando correctamente, verás que fastapi está ejecutandose, puedes ir a la documentación en http://127.0.0.1:8000/docs#/ o http://127.0.0.1:8000/redoc

¡Visita https://fastapi.tiangolo.com para la documentación completa!

##  Estructura del proyecto

  

/apps/backend

  

│
├── /app
│ ├── /api
│ │ ├── chat.py
│ │ ├── whatsapp.py
│ │ └── health.py
│ │
│ ├── /services (aquí vive la lógica de cada servicio)
│ │ ├── chat_service.py
│ │ ├── ai_client.py
│ │ └── whatsapp_service.py
│ │
│ ├── /core (aquí van las configuraciones)
│ │ └── config.py
│ │
│ ├── /models (aquí se definen las estructuras de datos con las que se trabaja y modela el back)
│ │ └── schemas.py
│ │
│ └── main.py
│
├── requirements.txt
└── README.md

  
  

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