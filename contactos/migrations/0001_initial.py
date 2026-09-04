from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="nombre")),
                ("phone", models.CharField(max_length=30, verbose_name="telefono")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="correo electronico")),
                ("address", models.TextField(verbose_name="direccion")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="fecha de creacion")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="ultima actualizacion")),
            ],
            options={
                "verbose_name": "contacto",
                "verbose_name_plural": "contactos",
                "ordering": ["name", "email"],
            },
        ),
    ]