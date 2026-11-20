# Agenda Clara

Agenda de contactos hecha con Django. Incluye una API REST protegida con JWT y
un cliente web React para iniciar sesión y gestionar contactos.

## Requisitos

- Python 3.10 o superior
- Node.js 20.19+ o 22.12+ para ejecutar el cliente React
- PostgreSQL si no vas a usar la base de datos SQLite local

## Ejecutar backend y frontend en local

Ejecuta cada parte en una terminal independiente de PowerShell y deja ambas
terminales abiertas mientras usas la aplicación. Los comandos de esta sección
parten desde la carpeta raíz del repositorio, que contiene las carpetas
`octaviogutierrez-eva1backend` y `front-end`.

### 1. Preparar e iniciar el backend

En la primera terminal:

```powershell
cd .\octaviogutierrez-eva1backend
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Edita `.env` y configura la conexión a PostgreSQL y `DJANGO_SECRET_KEY`. Si
quieres usar SQLite local, deja vacías las variables `DB_HOST`, `DB_PORT`,
`DB_NAME`, `DB_USER` y `DB_PASSWORD`. Conserva en `CLIENT_ORIGINS` el origen
local del frontend (`http://localhost:5500` y
`http://127.0.0.1:5500`).

Aplica las migraciones y, si aún no tienes un usuario, créalo:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Inicia Django:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Deja esta terminal abierta. Django debe indicar que está ejecutándose en
`http://127.0.0.1:8000/`.

### 2. Preparar e iniciar el frontend React

Abre una segunda terminal. Desde la raíz del repositorio:

```powershell
cd .\front-end
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
npm.cmd install
npm.cmd run dev
```

Comprueba que `front-end/.env` contenga:

```text
VITE_API_URL=http://127.0.0.1:8000
```

Abre la dirección **Local** que muestre Vite (normalmente
`http://localhost:5500`) e inicia sesión con el usuario Django. Usa la dirección
Local, no la dirección Network. Para que las peticiones lleguen a Django,
ambos servidores deben seguir ejecutándose.

Si el puerto 5500 está ocupado, no detengas un servicio desconocido. Inicia
Vite en el puerto 5510:

```powershell
npm.cmd run dev -- --host 127.0.0.1 --port 5510
```

Agrega `http://localhost:5510` y `http://127.0.0.1:5510` a
`CLIENT_ORIGINS` en el `.env` del backend y reinicia Django. Luego abre
`http://127.0.0.1:5510`.

Para instrucciones del cliente por separado, consulta
[el repositorio del frontend en GitHub](https://github.com/OctavioGutierrez20/front-end#readme).

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

La configuración de despliegue incluye `vercel.json` y `runtime.txt` para facilitar
la publicación del backend en Vercel. La URL pública esperada para la API es:
`https://octaviogutierrez-eva1backend.vercel.app`.

La API debe quedar accesible con los endpoints `/api/token/`, `/api/token/refresh/`
y `/api/contacts/` y responder con JSON válido. Este proyecto ya incluye CORS con
`django-cors-headers` para aceptar al cliente en `http://localhost:5500` y en el
origen real del despliegue.

## Pruebas

```powershell
.\.venv\Scripts\python.exe manage.py test --keepdb
```

Las pruebas cubren autenticación JWT, operaciones CRUD y CORS desde el cliente
local.
