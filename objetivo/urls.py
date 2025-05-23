from django.urls import path
from .views import ObjetivoCreateView, ObjetivoListCreateView, ObjetivoDetailView, ObjetivoDeleteView

urlpatterns = [
    path('objetivo/', ObjetivoListCreateView.as_view(), name='objetivo-list'),
    path('objetivo/create/', ObjetivoCreateView.as_view(), name='objetivo-create'),
    path('objetivo/<uuid:id>/', ObjetivoDetailView.as_view(), name='objetivo-detail'),
    path('objetivo/<uuid:id>/delete/', ObjetivoDeleteView.as_view(), name='objetivo-delete'),
]