from django.urls import path
from .views import PredictorView, MetricsView, PerformanceView, StatsView

urlpatterns = [
    path('predict/', PredictorView.as_view(), name='predict'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
    path('model-performance/', PerformanceView.as_view(), name='model-performance'),
    path('stats/', StatsView.as_view(), name='stats'),
]