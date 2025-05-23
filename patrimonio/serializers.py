from rest_framework import serializers
from .models import Patrimonio

class PatrimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patrimonio
        fields = ['id', 'nome', 'tipo', 'data_aquisicao', 'valor']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data.pop('user_id', None)
        patrimonio = Patrimonio.objects.create(user_id=user, **validated_data)

        return patrimonio
    
    def update(self, instance, validated_data):
        validated_data.pop('user_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance