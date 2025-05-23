import cloudinary
from rest_framework import serializers
from usuarios.models import CustomUser
from .models import Holding, Documento, Notificacao, Processo

class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = ['id', 'user_id', 'nome_holding', 'cnpj', 'status', 'criado_em']
        read_only_fields = ['id', 'user_id', 'criado_em']

    def validate_cnpj(self, value):
        if not value:
            raise serializers.ValidationError("CNPJ não pode estar vazio.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Holding.objects.filter(user_id=user).exists():
                raise serializers.ValidationError(
                    {"non_field_errors": ["Você já possui uma holding registrada."]}
                )
        return data

class DocumentoSerializer(serializers.ModelSerializer):
    arquivo = serializers.FileField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Documento
        fields = ['id', 'holding_id', 'user_id', 'tipo_documento', 'url_arquivo', 'status', 'data_envio', 'arquivo']
        read_only_fields = ['id', 'holding_id', 'user_id', 'url_arquivo', 'data_envio']

    def validate(self, data):
        user = self.context['request'].user
        try:
            holding = Holding.objects.get(user_id=user)
        except Holding.DoesNotExist:
            raise serializers.ValidationError(
                {"non_field_errors": ["Você precisa ter uma holding registrada para enviar documentos."]}
            )
        data['holding_id'] = holding
        return data

    def validate_tipo_documento(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("O tipo do documento não pode estar vazio.")
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Documento._meta.get_field('status').choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status deve ser um dos seguintes: {valid_statuses}")
        return value

    def validate_arquivo(self, value):
        if not value:
            return value
        allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
        max_size = 5 * 1024 * 1024  # 5MB
        if value.content_type not in allowed_types:
            raise serializers.ValidationError(
                "Tipo de arquivo não suportado. Use PDF, JPEG ou PNG."
            )
        if value.size > max_size:
            raise serializers.ValidationError("O arquivo não pode exceder 5MB.")
        return value

    def create(self, validated_data):
        arquivo = validated_data.pop('arquivo', None)
        if arquivo:
            try:
                upload_result = cloudinary.uploader.upload(
                    arquivo,
                    resource_type="raw",
                    folder="documentos",
                    access_mode="public"
                )
                validated_data['url_arquivo'] = upload_result['secure_url']
            except Exception as e:
                raise serializers.ValidationError({"arquivo": f"Erro ao fazer upload do arquivo: {str(e)}"})
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        arquivo = validated_data.pop('arquivo', None)
        if arquivo:
            try:
                if instance.url_arquivo:
                    public_id = self._extract_public_id(instance.url_arquivo)
                    if public_id:
                        cloudinary.uploader.destroy(public_id, resource_type="raw")
                upload_result = cloudinary.uploader.upload(
                    arquivo,
                    resource_type="raw",
                    folder="documentos",
                    access_mode="public"
                )
                validated_data['url_arquivo'] = upload_result['secure_url']
            except Exception as e:
                raise serializers.ValidationError({"arquivo": f"Erro ao fazer upload do arquivo: {str(e)}"})
        return super().update(instance, validated_data)

    def _extract_public_id(self, url):
        try:
            parts = url.split('/')
            folder_index = parts.index('documentos')
            public_id = '/'.join(parts[folder_index:])
            public_id = '.'.join(public_id.split('.')[:-1])
            return public_id
        except Exception as e:
            return None
        

class ProcessoSerializer(serializers.ModelSerializer):
    holding_id = serializers.UUIDField()  # Accept UUID as input

    class Meta:
        model = Processo
        fields = ['id', 'holding_id', 'etapa', 'status', 'data_inicio', 'data_fim']
        read_only_fields = ['id', 'data_inicio']

    def validate_holding_id(self, value):
        user = self.context['request'].user
        try:
            holding = Holding.objects.get(id=value, user_id=user)
        except Holding.DoesNotExist:
            raise serializers.ValidationError(
                "A holding especificada não existe ou não pertence ao usuário."
            )
        return value

    def validate_etapa(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A etapa não pode estar vazia.")
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Processo._meta.get_field('status').choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status deve ser um dos seguintes: {valid_statuses}")
        return value

    def create(self, validated_data):
        holding_id = validated_data.pop('holding_id')
        holding = Holding.objects.get(id=holding_id)
        return Processo.objects.create(holding_id=holding, **validated_data)

    def update(self, instance, validated_data):
        holding_id = validated_data.pop('holding_id', None)
        if holding_id:
            holding = Holding.objects.get(id=holding_id)
            instance.holding_id = holding
        return super().update(instance, validated_data)

class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ['id', 'user_id', 'mensagem', 'tipo', 'data_envio', 'is_lida']
        read_only_fields = ['id', 'user_id', 'data_envio']

    def validate_mensagem(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A mensagem não pode estar vazia.")
        return value

    def validate_tipo(self, value):
        valid_types = [choice[0] for choice in Notificacao._meta.get_field('tipo').choices]
        if value not in valid_types:
            raise serializers.ValidationError(f"Tipo deve ser um dos seguintes: {valid_types}")
        return value

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)