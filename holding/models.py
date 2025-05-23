import uuid
from django.db import models
from usuarios.models import CustomUser

class Holding(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='holding_user')
    nome_holding = models.CharField(max_length=255, verbose_name="Nome Holding")
    cnpj = models.CharField(max_length=30, verbose_name="CNPJ")
    status = models.CharField(
        max_length=30,
        verbose_name="Status",
        choices=[
            ('pending', 'Em análise'),
            ('approved', 'Aprovada'),
            ('rejected', 'Rejeitada'),
        ]
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_holding
    

class Documento(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holding_id = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='documento_holding')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documento_user')
    tipo_documento = models.CharField(max_length=100, verbose_name='Tipo do Documento') 
    url_arquivo = models.CharField(max_length=200, verbose_name='URL do Arquivo')
    status = models.CharField(
        max_length=30,
        verbose_name="Status",
        choices=[
            ('pending', 'Pendente'),
            ('sent', 'Enviado'),
            ('approved', 'Aprovado'),
            ('rejected', 'Rejeitado'),
        ],
    )
    data_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_envio']

    def __str__(self):
        return f"{self.tipo_documento} ({self.holding_id.nome_holding})"
    

class Processo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    holding_id = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='process_holding')
    etapa = models.CharField(max_length=50, verbose_name="Etapa")
    status = models.CharField(
        max_length=30,
        verbose_name="Status",
        choices=[
            ('pending', 'Pendente'),
            ('progress', 'Em andamento'),
            ('completed', 'Concluído'),
        ]
    )
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.holding_id} - ({self.etapa})"
    

class Notificacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notificacao_user')
    mensagem = models.TextField(max_length=1000, verbose_name="Mensagem")
    tipo = models.CharField(
        max_length=50,
        verbose_name="Tipo de Notificação",
        choices=[
            ('alert', 'Alerta'),
            ('update', 'Atualização'),
            ('request', 'Solicitação'),
        ]
    )
    data_envio = models.DateTimeField(auto_now_add=True)
    is_lida = models.BooleanField(default=False)

    class Meta:
        ordering = ['data_envio']

    def __str__(self):
        return f"{self.tipo}"