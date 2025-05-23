import cloudinary
import logging
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from usuarios.models import CustomUser
from .models import Holding, Documento, Processo, Notificacao
from .serializers import HoldingSerializer, DocumentoSerializer, ProcessoSerializer, NotificacaoSerializer

logger = logging.getLogger(__name__)

class HoldingListCreateView(generics.ListCreateAPIView):
    serializer_class = HoldingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Holding.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_id=user)
        user.tem_holding = True
        user.save()

    def get_serializer_context(self):
        return {'request': self.request}

class HoldingCreateView(generics.CreateAPIView):
    serializer_class = HoldingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_id=user)
        user.tem_holding = True
        user.save()

    def get_serializer_context(self):
        return {'request': self.request}

class HoldingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = HoldingSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Holding.objects.filter(user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

class DocumentoListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Documento.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {'request': self.request}

class DocumentoCreateView(generics.CreateAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {'request': self.request}

class DocumentoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Documento.objects.filter(user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        logger.info(f"Updating document ID: {self.get_object().id}")
        serializer.save()

class DocumentoDestroyView(generics.DestroyAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Documento.objects.filter(user_id=self.request.user)

    def perform_destroy(self, instance):
        try:
            if instance.url_arquivo:
                public_id = self._extract_public_id(instance.url_arquivo)
                if public_id:
                    logger.info(f"Deleting Cloudinary file: {public_id}")
                    cloudinary.uploader.destroy(public_id, resource_type="raw")
            instance.delete()
            logger.info(f"Deleted document ID: {instance.id}")
        except Exception as e:
            logger.error(f"Error deleting document ID {instance.id}: {str(e)}")
            raise

    def _extract_public_id(self, url):
        try:
            parts = url.split('/')
            folder_index = parts.index('documentos')
            public_id = '/'.join(parts[folder_index:])
            public_id = '.'.join(public_id.split('.')[:-1])
            return public_id
        except Exception as e:
            logger.error(f"Failed to extract public_id from URL {url}: {str(e)}")
            return None
        

class ProcessoListCreateView(generics.ListCreateAPIView):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Processo.objects.filter(holding_id__user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {'request': self.request}

class ProcessoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Processo.objects.filter(holding_id__user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        logger.info(f"Updating processo ID: {self.get_object().id}")
        serializer.save()

class ProcessoDestroyView(generics.DestroyAPIView):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Processo.objects.filter(holding_id__user_id=self.request.user)

    def perform_destroy(self, instance):
        logger.info(f"Deleting processo ID: {instance.id}")
        instance.delete()

class NotificacaoListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notificacao.objects.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {'request': self.request}

class NotificacaoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Notificacao.objects.filter(user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        logger.info(f"Updating notificacao ID: {self.get_object().id}")
        serializer.save()

class NotificacaoDestroyView(generics.DestroyAPIView):
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Notificacao.objects.filter(user_id=self.request.user)

    def perform_destroy(self, instance):
        logger.info(f"Deleting notificacao ID: {instance.id}")
        instance.delete()