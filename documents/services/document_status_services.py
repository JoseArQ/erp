from django.db import transaction   
from django.core.exceptions import ValidationError
from ..models import Document, DocumentStatus, DocumentStatusHistory


ALLOWED_TRANSITIONS = {
    DocumentStatus.PENDING: [DocumentStatus.APPROVED, DocumentStatus.REJECTED],
    DocumentStatus.APPROVED: [],
    DocumentStatus.REJECTED: [],
}

@transaction.atomic
def change_document_status(document: Document, new_status: str, user, comment: str = ""):
    """
    Changes the status of a document following the allowed state transitions.
    Also records the change in DocumentStatusHistory.

    Raises:
        ValidationError: If transition is not allowed.
    """
    old_status = document.status
    allowed = ALLOWED_TRANSITIONS.get(old_status, [])

    if new_status not in allowed:
        raise ValidationError(
            f"Invalid transition from '{old_status}' to '{new_status}'. Allowed: {allowed}"
        )

    document.status = new_status
    document.save(update_fields=["status"])

    DocumentStatusHistory.objects.create(
        document=document,
        previous_status=old_status,
        new_status=new_status,
        changed_by=user,
        comment=comment,
    )

    return document
