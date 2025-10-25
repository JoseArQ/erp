import uuid
from django.conf import settings
from django.db import models
from company.models import Company


class EntityType(models.TextChoices):
    VEHICLE  = "vehicle", "Vehicle"
    EMPLOYEE = "employee", "Employee"
    OTHER = "other", "Other"


class Entity(models.Model):
    """
    Represents a business entity to which documents can be linked.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=50, choices=EntityType.choices, default=EntityType.OTHER)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="entities")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} ({self.id})"

class DocumentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class Document(models.Model):
    """
    Represents a document belonging to a company and linked to a specific entity.
    The file is managed by a pluggable DocumentManager backend.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=500, help_text="Storage path or key of the file")
    doc_type = models.CharField(max_length=100)
    size = models.PositiveBigIntegerField()
    mime_type = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="documents")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="documents")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_documents"
    )
    status = models.CharField(
        max_length=20,
        choices=DocumentStatus.choices,
        default=DocumentStatus.PENDING.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class DocumentStatusHistory(models.Model):
    """
    Tracks the history of document status changes.
    """
    document = models.ForeignKey(
        Document, 
        on_delete=models.CASCADE, 
        related_name="status_history",
        )
    previous_status = models.CharField(
        max_length=20, 
        choices=DocumentStatus.choices,
        )
    new_status = models.CharField(
        max_length=20, 
        choices=DocumentStatus.choices,
        )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="document_status_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.document.name}: {self.previous_status} → {self.new_status}"
