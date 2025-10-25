from rest_framework import serializers

from company.services import get_company

from .models import Entity
from .services import document_services, entity_services

class EntitySerializer(serializers.Serializer):
    """Serializer for validating and retrieving an existing Entity."""
    
    id = serializers.UUIDField()
    type = serializers.CharField(max_length=100, required=False, read_only=True)

    def validate(self, data):
        """
        Validate that the Entity exists and attach the instance.
        """
        entity = entity_services.get_entity({"id": data["id"]})
        data["instance"] = entity  
        return data

class CompanySerializer(serializers.Serializer):
    """Serializer for validating and retrieving an existing Company."""
    
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255, required=False, read_only=True)

    def validate(self, data):
        """
        Validate that the Company exists and attach the instance.
        """
        company = get_company({"id": data["id"]})
        data["instance"] = company
        return data
    
class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    doc_type = serializers.CharField(max_length=100)
    entity = EntitySerializer()
    company = CompanySerializer()

    def create(self, validated_data):
        request = self.context["request"]
        entity_data = validated_data.pop("entity")
        company_data = validated_data.pop("company")

        entity = entity_data["instance"]
        company = company_data["instance"]

        return document_services.create_document(
            file=validated_data["file"],
            company=company,
            entity=entity,
            user=request.user,
            doc_type=validated_data["doc_type"],
        )

class DocumentStatusUpdateSerializer(serializers.Serializer):
    """Serializer for approving or rejecting a document with an optional comment."""
    
    comment = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text="Optional comment describing the reason for approval or rejection."
    )