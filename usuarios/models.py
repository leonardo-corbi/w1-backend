import uuid 
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="Email")
    nome = models.CharField(max_length=100, verbose_name="Nome")
    sobrenome = models.CharField(max_length=100, verbose_name="Sobrenome")
    telefone = models.CharField(max_length=20, verbose_name="Telefone") 
    cargo = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('client', 'Cliente')
        ],
        default='client',
        verbose_name="Cargo"
    )
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")

    # Endereço
    cep = models.CharField(max_length=9, verbose_name="CEP")
    rua = models.CharField(max_length=200, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    estado = models.CharField(
        max_length=2, 
        choices=[
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        ], 
        verbose_name="Estado"
    )

    # Dados Financeiros
    renda_mensal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Renda Mensal")
    tem_patrimonio = models.BooleanField(default=False)
    patrimonio = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Patrimônio", null=True, blank=True)
    conhecimento_investimento = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Iniciante'),
            ('intermediate', 'Intermediário'),
            ('advanced', 'Avançado'),
        ],
        default='beginner',
        verbose_name='Conhecimento em Investimento',
    )
    aceita_termos = models.BooleanField(default=False, verbose_name='Aceita Termos')
    data_contratacao = models.DateTimeField(blank=True, null=True, verbose_name="Data de Contratação")
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    is_verified = models.BooleanField(default=False, verbose_name='Verificado')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    tem_holding = models.BooleanField(default=False, verbose_name="Tem Holding")
    data_registro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(blank=True, null=True, verbose_name='Data de Atualização')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'nome',
        'sobrenome',
        'telefone',
        'cargo',
        'cpf',
        'data_nascimento',
        'cep',
        'rua',
        'numero',
        'bairro',
        'cidade',
        'estado',
        'renda_mensal',
        'tem_patrimonio',
        'conhecimento_investimento',
        'aceita_termos'
    ]

    class Meta:
        verbose_name = 'Usuário',
        verbose_name_plural = 'Usuários',
        ordering = ['-data_registro']

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f'{self.nome} {self.sobrenome}'
    
    def get_short_name(self): 
        return self.nome