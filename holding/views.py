import cloudinary, uuid
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.core.exceptions import ValidationError
from usuarios.models import CustomUser
from .models import Holding, Documento, Processo, Notificacao
from .serializers import HoldingSerializer, DocumentoSerializer, ProcessoSerializer, NotificacaoSerializer


class HoldingListCreateView(generics.ListCreateAPIView):
    serializer_class = HoldingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            if not self.request.user.is_staff:
                raise PermissionDenied("Apenas administradores podem acessar dados de outros usuários.")
            try:
                uuid_obj = uuid.UUID(user_id)
                queryset = Holding.objects.filter(user_id=user_id)
    
                return queryset
            except (ValueError, ValidationError) as e:

                return Holding.objects.none()
        queryset = Holding.objects.filter(user_id=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

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
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Holding.objects.all()
        return Holding.objects.filter(user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

class DocumentoListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            if not self.request.user.is_staff:
                raise PermissionDenied("Apenas administradores podem acessar dados de outros usuários.")
            try:
                uuid_obj = uuid.UUID(user_id)
                queryset = Documento.objects.filter(user_id=user_id)
    
                return queryset
            except (ValueError, ValidationError) as e:
    
                return Documento.objects.none()
        queryset = Documento.objects.filter(user_id=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

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
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Documento.objects.all()
        return Documento.objects.filter(user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
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
                    cloudinary.uploader.destroy(public_id, resource_type="raw")
            instance.delete()
        except Exception as e:
            raise

    def _extract_public_id(self, url):
        try:
            parts = url.split('/')
            folder_index = parts.index('documentos')
            public_id = '/'.join(parts[folder_index:])
            public_id = '.'.join(public_id.split('.')[:-1])
            return public_id
        except Exception as e:
            return None
        

class ProcessoListCreateView(generics.ListCreateAPIView):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            if not self.request.user.is_staff:
                raise PermissionDenied("Apenas administradores podem acessar dados de outros usuários.")
            try:
                uuid_obj = uuid.UUID(user_id)
                queryset = Processo.objects.filter(user_id=user_id)
                
                return queryset
            except (ValueError, ValidationError) as e:
                
                return Processo.objects.none()
        queryset = Processo.objects.filter(user_id=self.request.user)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class ProcessoRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Processo.objects.filter(holding_id__user_id=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_update(self, serializer):
        serializer.save()

class ProcessoDestroyView(generics.DestroyAPIView):
    serializer_class = ProcessoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Processo.objects.filter(holding_id__user_id=self.request.user)

    def perform_destroy(self, instance):
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
        serializer.save()

class NotificacaoDestroyView(generics.DestroyAPIView):
    serializer_class = NotificacaoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Notificacao.objects.filter(user_id=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()