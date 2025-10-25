import os
from django.conf import settings
from .base import DocumentManager


class DocumentLocal(DocumentManager):
    """
    Local filesystem implementation of DocumentManager.
    Files are saved under MEDIA_ROOT/documents/<company>/<entity>/<filename>.
    """

    def upload(self, file_obj, company_id: int, entity_reference: str, filename: str) -> str:
        folder = os.path.join(settings.MEDIA_ROOT, "documents", str(company_id), entity_reference)
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)

        with open(path, "wb+") as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Return the relative path (to MEDIA_ROOT)
        rel_path = os.path.relpath(path, settings.MEDIA_ROOT)
        return rel_path

    def download(self, path: str):
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return open(file_path, "rb")
