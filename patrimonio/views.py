from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import PatrimonioSerializer
from .models import Patrimonio


class PatrimonioListCreateView(generics.ListCreateAPIView):
    serializer_class = PatrimonioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patrimonio.objects.filter(user_id=self.request.user)
    

class PatrimonioDetailView(generics.RetrieveUpdateAPIView):  
    serializer_class = PatrimonioSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Patrimonio.objects.filter(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
    

class PatrimonioCreateView(generics.CreateAPIView):
    serializer_class = PatrimonioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class PatrimonioDeleteView(generics.DestroyAPIView):
    serializer_class = PatrimonioSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Patrimonio.objects.filter(user_id=self.request.user)

    def perform_destroy(self, instance):    
        instance.delete()
