from rest_framework import serializers
from .models import Objetivo

class ObjetivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objetivo
        fields = ['id', 'titulo', 'descricao', 'categoria', 'valor_alvo',
                  'valor_atual', 'data_alvo', 'aporte_mensal', 'prioridade',
                  'status', 'criado_em']
        read_only_fields = ['id', 'criado_em']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user_id', None) 
        objetivo = Objetivo.objects.create(user_id=user, **validated_data)
        return objetivo
    
    def update(self, instance, validated_data):
        validated_data.pop('user_id', None)  
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance