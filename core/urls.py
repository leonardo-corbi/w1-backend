from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api/', include('patrimonio.urls')),
    path('api/', include('objetivo.urls')),
    path('api/', include('holding.urls')),
]
