# api/models.py
import uuid
from django.db import models
from usuarios.models import CustomUser

class Objetivo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='objetivos')
    titulo = models.CharField(max_length=255, verbose_name="Titulo")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    categoria = models.CharField(
        max_length=100, 
        verbose_name="Categoria",
        choices=[
            ('retirement', 'Aposentadoria'),
            ('travel', 'Viagem'),
            ('real_estate', 'Imóvel'),
            ('vehicle', 'Veículo'),
            ('education', 'Educação'),
            ('health', 'Saúde'),
            ('business', 'Negócio'),
            ('other', 'Outro')
        ]
    )
    valor_alvo = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Alvo")
    valor_atual = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Atual", default=0)
    data_alvo = models.DateField(verbose_name="Data Alvo")
    aporte_mensal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Aporte Mensal", default=0)
    prioridade = models.CharField(
        max_length=10,
        verbose_name="Prioridade",
        choices=[
            ('baixa', 'Baixa'),
            ('media', 'Média'),
            ('alta', 'Alta')
        ],
        default='media'
    )
    status = models.CharField(
        max_length=100, 
        verbose_name="Status",
        choices=[
            ('pending', 'Pendente'),
            ('processing', 'Em processo'),
            ('completed', 'Concluído')
        ],
        default='pending'
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return self.titulo