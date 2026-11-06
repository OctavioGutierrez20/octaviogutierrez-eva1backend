from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

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


class ContactApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="api-user",
            password="test-password-123",
        )
        self.client = APIClient()

    def test_contacts_require_authentication(self):
        response = self.client.get("/api/contacts/")
        self.assertEqual(response.status_code, 401)

    def test_jwt_token_and_contact_crud(self):
        token_response = self.client.post(
            "/api/token/",
            {"username": "api-user", "password": "test-password-123"},
            format="json",
        )
        self.assertEqual(token_response.status_code, 200)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )
        contact_data = {
            "name": "Ana Perez",
            "phone": "+56912345678",
            "email": "ana@example.com",
            "address": "Av. Central 123",
        }

        create_response = self.client.post(
            "/api/contacts/",
            contact_data,
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        contact_id = create_response.data["id"]

        list_response = self.client.get("/api/contacts/")
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        update_response = self.client.patch(
            f"/api/contacts/{contact_id}/",
            {"name": "Ana Soto"},
            format="json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["name"], "Ana Soto")

        delete_response = self.client.delete(f"/api/contacts/{contact_id}/")
        self.assertEqual(delete_response.status_code, 204)

    def test_cors_allows_local_web_client(self):
        response = self.client.options(
            "/api/contacts/",
            HTTP_ORIGIN="http://localhost:5500",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        self.assertEqual(
            response["Access-Control-Allow-Origin"],
            "http://localhost:5500",
        )