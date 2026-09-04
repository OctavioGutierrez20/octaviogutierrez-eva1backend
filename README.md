# Agenda Clara

Aplicacion Django para gestionar una agenda de contactos personales. Implementa el
caso 3 de la evaluacion de Programacion Backend: agregar contactos con nombre,
telefono, correo y direccion; buscar por nombre o correo; y validar el formato del
correo electronico.

## Requisitos

- Python 3.10 o superior
- Django 5

## Instalacion y ejecucion

```bash
python -m venv .venv
# En Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000/` en el navegador.

## Funcionalidades

- Crear, editar y eliminar contactos.
- Buscar contactos por nombre o correo electronico.
- Validar nombre, telefono, direccion y correo con formularios Django.
- Persistir la informacion en SQLite.
- Administrar contactos desde `/admin/`.

Para ejecutar las pruebas:

```bash
python manage.py test
```

