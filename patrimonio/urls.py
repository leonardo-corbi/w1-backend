from django.urls import path
from .views import PatrimonioCreateView, PatrimonioListCreateView, PatrimonioDetailView, PatrimonioDeleteView

urlpatterns = [
    path('patrimonio/', PatrimonioListCreateView.as_view(), name='patrimonio-list'),
    path('patrimonio/create/', PatrimonioCreateView.as_view(), name='patrimonio-create'),
    path('patrimonio/<uuid:id>/', PatrimonioDetailView.as_view(), name='patrimonio-detail'),
    path('patrimonio/<uuid:id>/delete/', PatrimonioDeleteView.as_view(), name='patrimonio-delete'),
]