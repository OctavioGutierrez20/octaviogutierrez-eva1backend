from pathlib import Path
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv("DEBUG", "True").lower() == "true"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Define DJANGO_SECRET_KEY antes de desplegar.")
    SECRET_KEY = "django-insecure-agenda-contactos-local"

allowed_hosts = os.getenv("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [
    host.strip()
    for host in allowed_hosts.split(",")
    if host.strip()
]
ALLOWED_HOSTS.extend([
    'octaviogutierrez-eva1backend.vercel.app',
    '.vercel.app',
    'localhost',
    '127.0.0.1',
])

client_origins = os.getenv("CLIENT_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500")
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in client_origins.split(",")
    if origin.strip()
]
CORS_ALLOWED_ORIGINS.extend([
    "https://octaviogutierrez-eva1backend.vercel.app",
    "https://front-end-pearl-five.vercel.app",
    "https://front-end-back-end8.vercel.app",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:5510",
    "http://127.0.0.1:5510",
])
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in CORS_ALLOWED_ORIGINS
    if origin.strip()
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

db_host = os.getenv("DB_HOST") or os.getenv("host")
db_port = os.getenv("DB_PORT") or os.getenv("port")
db_database = os.getenv("DB_NAME") or os.getenv("database")
db_user = os.getenv("DB_USER") or os.getenv("user")
db_password = os.getenv("DB_PASSWORD") or os.getenv("password")
database_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL")
if database_url:
    parsed = urlparse(database_url)
    db_host = parsed.hostname or db_host
    db_port = parsed.port or db_port
    db_database = parsed.path.lstrip("/") or db_database
    db_user = parsed.username or db_user
    db_password = parsed.password or db_password

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "contactos",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':(
        'rest_framework.permissions.IsAuthenticated',
    )
}

ROOT_URLCONF = "agenda_contactos.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "agenda_contactos.wsgi.application"

if all([db_host, db_port, db_database, db_user, db_password]):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": db_database,
            "USER": db_user,
            "PASSWORD": db_password,
            "HOST": db_host,
            "PORT": db_port,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}