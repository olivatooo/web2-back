from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.IntegerField(blank=False, unique=False, null=True)

    class Meta:
        verbose_name_plural = "Usuário"
        verbose_name = "Usuário"


class SiteReserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, blank=False, unique=True)
    telefone = models.CharField(max_length=20, blank=False, unique=True)


    class Meta:
        verbose_name_plural = "Sites de Reserva"
        verbose_name = "Site de Reserva"

    def __str__(self):
        return self.nome


class Hotel(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30, blank=False, unique=True)
    cidade = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        first = False
        if self.pk is None:
            first = True
        super().save(*args, **kwargs)
        if first:
            Token.objects.create(user=self.usuario)


class Promocao(models.Model):
    site = models.ForeignKey(SiteReserva, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    def __str__(self):
        return f"{self.site} - {self.hotel}"

    class Meta:
        verbose_name_plural = "Promoção"
        verbose_name = "Promoções"
