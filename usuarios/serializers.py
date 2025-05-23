import re
from datetime import date
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'nome', 'sobrenome', 'telefone', 'cpf', 'data_nascimento',
            'cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'renda_mensal', 'tem_patrimonio', 'conhecimento_investimento'
        ]
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'email', 'password', 'password_confirm', 'nome', 'sobrenome', 'telefone', 'cpf', 'data_nascimento',
            'cep', 'rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'renda_mensal', 'tem_patrimonio', 'conhecimento_investimento', 'aceita_termos'
        ]
        extra_kwargs = {
            'nome': {'required': True},
            'sobrenome': {'required': True},
            'cpf': {'required': True},
            'data_nascimento': {'required': True},
            'telefone': {'required': True},
            'cep': {'required': True},
            'rua': {'required': True},
            'numero': {'required': True},
            'bairro': {'required': True},
            'cidade': {'required': True},
            'estado': {'required': True},
            'renda_mensal': {'required': True},
            'aceita_termos': {'required': True},
        }

    def validate(self, attrs):
        # Validação de senha
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'As senhas não são iguais.'})

        # Validação de CPF (formato 000.000.000-00)
        cpf = attrs.get('cpf', '')
        if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
            raise serializers.ValidationError({'cpf': 'CPF inválido. Use o formato 000.000.000-00.'})
        
        # Validação de telefone
        telefone = attrs.get('telefone', '')
        if not re.match(r'^\+?\d{2}\s?\(\d{2}\)\s?\d{4,5}-\d{4}$', telefone):
            raise serializers.ValidationError('Telefone inválido. Use o formato +55 (11) 99999-9999.')

        # Validação de data de nascimento
        data_nascimento = attrs.get('data_nascimento')
        if data_nascimento:
            today = date.today()
            age = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
            if age < 18:
                raise serializers.ValidationError({'data_nascimento': 'O usuário deve ter pelo menos 18 anos.'})

        # Validação de aceite de termos
        if not attrs.get('aceita_termos', False):
            raise serializers.ValidationError({'aceita_termos': 'Você deve aceitar os termos de uso.'})

        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')

        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            nome=validated_data['nome'],
            sobrenome=validated_data['sobrenome'],
            cpf=validated_data['cpf'],
            data_nascimento=validated_data['data_nascimento'],
            telefone=validated_data['telefone'],
            cep=validated_data['cep'],
            rua=validated_data['rua'],
            numero=validated_data['numero'],
            complemento=validated_data.get('complemento', ''),
            bairro=validated_data['bairro'],
            cidade=validated_data['cidade'],
            estado=validated_data['estado'],
            renda_mensal=validated_data.get('renda_mensal'),
            conhecimento_investimento=validated_data.get('conhecimento_investimento', 'beginner'),
            aceita_termos=validated_data.get('aceita_termos', False),
            data_atualizacao=timezone.now()
        )
        return user

    
