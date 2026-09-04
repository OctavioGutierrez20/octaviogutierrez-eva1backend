from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm
from .models import Contact


class ContactFormTests(TestCase):
    def test_rejects_invalid_email(self):
        form = ContactForm(data={"name": "Ana Perez", "phone": "+56912345678", "email": "correo-invalido", "address": "Av. Central 123"})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_accepts_valid_contact(self):
        form = ContactForm(data={"name": "Ana Perez", "phone": "+56912345678", "email": "ana@example.com", "address": "Av. Central 123"})
        self.assertTrue(form.is_valid())


class ContactViewsTests(TestCase):
    def setUp(self):
        Contact.objects.create(name="Ana Perez", phone="+56912345678", email="ana@example.com", address="Av. Central 123")

    def test_list_searches_by_name_or_email(self):
        response = self.client.get(reverse("contactos:list"), {"q": "ana@example"})
        self.assertContains(response, "Ana Perez")

    def test_create_contact(self):
        response = self.client.post(reverse("contactos:create"), {"name": "Luis Soto", "phone": "+56987654321", "email": "luis@example.com", "address": "Los Robles 45"})
        self.assertRedirects(response, reverse("contactos:list"))
        self.assertTrue(Contact.objects.filter(email="luis@example.com").exists())

    def test_duplicate_email_is_rejected(self):
        response = self.client.post(reverse("contactos:create"), {"name": "Otra Persona", "phone": "+56987654321", "email": "ana@example.com", "address": "Los Robles 45"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.context["form"].errors)