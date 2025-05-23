from django.urls import path
from .views import (
    HoldingListCreateView,
    HoldingCreateView,
    HoldingDetailView,
    DocumentoListCreateView,
    DocumentoCreateView,
    DocumentoRetrieveUpdateView,
    DocumentoDestroyView,
    ProcessoListCreateView,
    ProcessoRetrieveUpdateView,
    ProcessoDestroyView,
    NotificacaoListCreateView,
    NotificacaoRetrieveUpdateView,
    NotificacaoDestroyView
)

urlpatterns = [
    path('holding/', HoldingListCreateView.as_view(), name='holding-list-create'),
    path('holding/create/', HoldingCreateView.as_view(), name='holding-create'),
    path('holding/<str:id>/', HoldingDetailView.as_view(), name='holding-detail'),
    
    # Documentos para Holding
    path('documento/', DocumentoListCreateView.as_view(), name='documento-list-create'),
    path('documento/create/', DocumentoCreateView.as_view(), name='documento-create'),
    path('documento/<str:id>/', DocumentoRetrieveUpdateView.as_view(), name='documento-retrieve-update'),
    path('documento/<str:id>/delete/', DocumentoDestroyView.as_view(), name='documento-destroy'),

    # Processos para Holding
    path('processo/', ProcessoListCreateView.as_view(), name='processo-list-create'),
    path('processo/<str:id>/', ProcessoRetrieveUpdateView.as_view(), name='processo-retrieve-update'),
    path('processo/<str:id>/delete/', ProcessoDestroyView.as_view(), name='processo-destroy'),

    # Notificação para cliente
    path('notificacao/', NotificacaoListCreateView.as_view(), name='notificacao-list-create'),
    path('notificacao/<str:id>/', NotificacaoRetrieveUpdateView.as_view(), name='notificacao-retrieve-update'),
    path('notificacao/<str:id>/delete/', NotificacaoDestroyView.as_view(), name='notificacao-destroy'),
]
