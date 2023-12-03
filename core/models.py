from django.db import models
from django.contrib.auth.models import User

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Acidente(models.Model):
    num_boletim = models.CharField(max_length=255, db_column='num_boletim', primary_key=True)
    data_hora_boletim = models.CharField(max_length=255, db_column='data_hora_boletim')
    Nº_envolvido = models.IntegerField(db_column='Nº_envolvido')
    condutor = models.CharField(max_length=255, db_column='condutor')
    cod_severidade = models.IntegerField(db_column='cod_severidade')
    desc_severidade = models.CharField(max_length=255, db_column='desc_severidade')
    sexo = models.CharField(max_length=255, db_column='sexo')
    cinto_seguranca = models.CharField(max_length=255, db_column='cinto_seguranca')
    Embreagues = models.CharField(max_length=255, db_column='Embreagues')
    Idade = models.IntegerField(db_column='Idade')
    nascimento = models.CharField(max_length=255, db_column='nascimento')
    categoria_habilitacao = models.CharField(max_length=255, db_column='categoria_habilitacao')
    descricao_habilitacao = models.CharField(max_length=255, db_column='descricao_habilitacao')
    declaracao_obito = models.CharField(max_length=255, db_column='declaracao_obito')
    cod_severidade_antiga = models.CharField(max_length=255, db_column='cod_severidade_antiga')
    especie_veiculo = models.CharField(max_length=255, db_column='especie_veiculo')
    pedestre = models.CharField(max_length=255, db_column='pedestre')
    passageiro = models.CharField(max_length=255, db_column='passageiro')

    def __str__(self):
        return self.num_boletim

    class Meta:
        db_table = 'acidente'


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=255)
    descricao = models.TextField()

