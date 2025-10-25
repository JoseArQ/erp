
import mimetypes

from company.models import Company

from ..models import Document, Entity
from ..storage.local import DocumentLocal

document_manager = DocumentLocal()

def create_document(file, company : Company, entity: Entity, user, doc_type: str) -> Document:
    """
    Handles document upload and creation linked to a business entity.
    """
    filename = file.name
    mime_type, _ = mimetypes.guess_type(filename)
    path = document_manager.upload(file, company.id, str(entity.id), filename)

    document = Document.objects.create(
        name=filename,
        path=path,
        doc_type=doc_type,
        size=file.size,
        mime_type=mime_type or "application/octet-stream",
        company=company,
        entity=entity,
        created_by=user,
        )
    return document


def download_document(document: Document) -> bytes:
    """Retrieve a stored document."""
    return document_manager.download(document.path)

def get_document(pk) -> Document:
    return Document.objects.get(pk=pk)