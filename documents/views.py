from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdmin, IsAdminOrEmployee

from common.responses import responses

from .models import Document, DocumentStatus
from .serializers import DocumentUploadSerializer, DocumentStatusUpdateSerializer
from .services import document_services, document_status_services


class DocumentsViewSet(viewsets.ViewSet):
    """
    Document upload/download/approval with pluggable storage backend.
    """

    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Upload a new document (accessible by admin and employee).
        """
        if not IsAdminOrEmployee().has_permission(request, self):
            return responses.error_response(
                message="Permission denied.", 
                status=status.HTTP_403_FORBIDDEN,
                )
        
        serializer = DocumentUploadSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        
        document = serializer.save()
        return responses.success_response(
            data={
                "id": document.id, 
                "path": document.path,
                }, 
            status_code=status.HTTP_201_CREATED,
            )
       

    def retrieve(self, request, pk=None):
        """
        Retrieve a document (accessible by admin and employee).
        """
        if not IsAdminOrEmployee().has_permission(request, self):
            return  responses.error_response(
                message="Permission denied.", 
                status=status.HTTP_403_FORBIDDEN,
                )
        
        try:
            document = document_services.get_document(pk)
        except Document.DoesNotExist:
            return responses.error_response(
                message="document not found", 
                status=status.HTTP_404_NOT_FOUND,
                )

        return responses.success_response(
            data={
                "document_path" : document.path
                }, 
            status_code=status.HTTP_200_OK,
            )

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        document = document_services.get_document(pk=pk)
        document_serializer = DocumentStatusUpdateSerializer(data=request.data)
        document_serializer.is_valid(raise_exception=True)
        comment = document_serializer.validated_data.get("comment", None)
        
        _ = document_status_services.change_document_status(
            document, DocumentStatus.APPROVED, request.user, comment=comment
        )

        return responses.success_response(
            data=None, 
            status_code=status.HTTP_200_OK,
            )

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        document = document_services.get_document(pk=pk)
        document_serializer = DocumentStatusUpdateSerializer(data=request.data)
        document_serializer.is_valid(raise_exception=True)
        comment = document_serializer.validated_data.get("comment", None)
        
        _ = document_status_services.change_document_status(
            document, DocumentStatus.REJECTED, request.user, comment=comment
        )

        return responses.success_response(
            data=None, 
            status_code=status.HTTP_200_OK,
            )