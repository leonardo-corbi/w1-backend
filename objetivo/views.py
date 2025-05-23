from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import render
from .serializers import ObjetivoSerializer
from .models import Objetivo


class ObjetivoListCreateView(generics.ListCreateAPIView):
    serializer_class = ObjetivoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Objetivo.objects.filter(user_id=self.request.user)
    

class ObjetivoDetailView(generics.RetrieveUpdateAPIView):  
    serializer_class = ObjetivoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Objetivo.objects.filter(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
    

class ObjetivoCreateView(generics.CreateAPIView):
    serializer_class = ObjetivoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class ObjetivoDeleteView(generics.DestroyAPIView):
    serializer_class = ObjetivoSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Objetivo.objects.filter(user_id=self.request.user)

    def perform_destroy(self, instance):    
        instance.delete()
