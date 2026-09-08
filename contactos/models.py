from django.db import models


class Contact(models.Model):
    name = models.CharField("nombre", max_length=120)
    phone = models.CharField("telefono", max_length=30, default='+56 9')
    email = models.EmailField("correo electronico", unique=True)
    address = models.TextField("direccion")
    created_at = models.DateTimeField("fecha de creacion", auto_now_add=True)
    updated_at = models.DateTimeField("ultima actualizacion", auto_now=True)

    class Meta:
        ordering = ["name", "email"]
        verbose_name = "contacto"
        verbose_name_plural = "contactos"

    def __str__(self):
        return f"{self.name} - {self.email}"