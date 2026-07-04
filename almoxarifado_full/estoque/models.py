from django.db import models
from django.contrib.auth.models import User


# CATEGORIAS

class Categoria(models.Model):

    nome = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):

        return self.nome


# ITENS

class Item(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nome = models.CharField(
        max_length=100
    )

    codigo = models.CharField(
        max_length=50
    )

    quantidade = models.IntegerField()

    valor_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def valor_total(self):

        return (
            self.quantidade *
            self.valor_unitario
        )

    def __str__(self):

        return self.nome