from abc import ABC, abstractmethod

class DocumentManager(ABC):
    """
    Abstract interface for managing document storage backends.
    """

    @abstractmethod
    def upload(self, file_obj, company_id: int, entity_reference: str, filename: str) -> str:
        """
        Upload a file and return its storage path or key.
        """
        pass

    @abstractmethod
    def download(self, path: str) -> bytes:
        """
        Retrieve the content of the stored file as bytes.
        """
        pass
