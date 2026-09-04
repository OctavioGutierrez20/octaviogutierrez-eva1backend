from django import forms

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "phone", "email", "address"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Ej: Ana Perez"}),
            "phone": forms.TextInput(attrs={"placeholder": "+56 9 1234 5678"}),
            "email": forms.EmailInput(attrs={"placeholder": "ana@ejemplo.cl"}),
            "address": forms.Textarea(attrs={"placeholder": "Calle, numero y comuna", "rows": 3}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("El nombre debe tener al menos 2 caracteres.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = sum(character.isdigit() for character in phone)
        if digits < 7:
            raise forms.ValidationError("Ingresa un telefono valido con al menos 7 digitos.")
        return phone

    def clean_address(self):
        address = self.cleaned_data["address"].strip()
        if len(address) < 5:
            raise forms.ValidationError("La direccion debe tener al menos 5 caracteres.")
        return address