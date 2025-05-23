import uuid
from django.db import models
from usuarios.models import CustomUser

class Patrimonio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patrimonios')
    nome = models.CharField(max_length=255, verbose_name="Nome")
    tipo = models.CharField(max_length=255, verbose_name="Tipo")
    data_aquisicao = models.DateField(verbose_name="Data de Aquisição")
    valor = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor")

    class Meta:
        verbose_name = "Patrimônio"
        verbose_name_plural = "Patrimônios"

    def __str__(self):
        return f"{self.nome} - {self.user_id.email}"
