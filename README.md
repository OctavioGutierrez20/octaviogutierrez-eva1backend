# Agenda Clara

Agenda de contactos hecha con Django. Incluye una API REST protegida con JWT y
un cliente web sencillo que permite iniciar sesión y gestionar contactos.

## Requisitos

- Python 3.10 o superior
- PostgreSQL

## Preparar el backend

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Completa en `.env` los datos de conexión a PostgreSQL y define una clave privada
para `DJANGO_SECRET_KEY`. Luego ejecuta:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

El backend queda disponible en `http://127.0.0.1:8000/`.

## Ejecutar el cliente web

Abre otra terminal en la carpeta del proyecto y ejecuta:

```powershell
python -m http.server 5500 --directory cliente
```

Abre `http://localhost:5500`. Inicia sesión con el usuario Django creado arriba.
El cliente obtiene el token JWT y permite listar, crear, editar y eliminar
contactos desde la API.

Si el backend está en otra dirección, cambia `API_URL` al inicio de
`cliente/app.js`. Para ejecutar el cliente desde otra dirección, agrega su origen
exacto a `CLIENT_ORIGINS` en `.env` y reinicia Django.

## API

- `POST /api/token/`: obtener access y refresh tokens.
- `POST /api/token/refresh/`: renovar el access token.
- `/api/contacts/`: listar y crear contactos.
- `/api/contacts/<id>/`: consultar, editar y eliminar un contacto.

Las rutas de contactos requieren el encabezado
`Authorization: Bearer <access-token>`.

## Despliegue

Al desplegar, configura las variables de entorno de PostgreSQL, `DJANGO_SECRET_KEY`,
`DEBUG=False` y `CLIENT_ORIGINS` con el origen real del cliente. Comprueba que el
dominio del backend esté en `ALLOWED_HOSTS`.

El dominio del backend configurado en el proyecto es
`https://octaviogutierrez-eva1backend.vercel.app`. Al probar la API durante esta
implementación respondió con error 500; hay que revisar las variables y los logs
del despliegue y volver a desplegar antes de presentar la URL como operativa.

## Pruebas

```powershell
python manage.py test --keepdb
```

Las pruebas cubren autenticación JWT, operaciones CRUD y CORS desde el cliente
local.
