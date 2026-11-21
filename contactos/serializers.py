from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "address",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )
        return value

    def validate_phone(self, value):
        value = value.strip()
        if sum(character.isdigit() for character in value) < 7:
            raise serializers.ValidationError(
                "El teléfono debe tener al menos 7 dígitos."
            )
        return value

    def validate_address(self, value):
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError(
                "La dirección debe tener al menos 5 caracteres."
            )
        return value
