from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class Usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.IntegerField(blank=False, unique=False, null=True)

    class Meta:
        verbose_name_plural = "Usuário"
        verbose_name = "Usuário"

    def __str__(self):
        return str(self.usuario) + " " + str(self.tipo)

class SiteReserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=False, unique=True)
    senha = models.CharField(max_length=255, blank=False, unique=False)
    nome = models.CharField(max_length=255, blank=False, unique=True)
    telefone = models.CharField(max_length=20, blank=False, unique=True)


    class Meta:
        verbose_name_plural = "Sites de Reserva"
        verbose_name = "Site de Reserva"

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        first = False
        if self.pk is None:
            first = True
        if first:
            user = User.objects.create_user(
                username=self.url,
                email=self.url + '@site.com',
                password=self.senha)
            usuario = Usuario(usuario=user, tipo=1)
            usuario.save()
            self.usuario = usuario
            Token.objects.create(user=user)
        super().save(*args, **kwargs)


class Hotel(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=255, blank=False, unique=True)
    senha = models.CharField(max_length=255, blank=False, unique=False)
    nome = models.CharField(max_length=30, blank=False, unique=True)
    cidade = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        first = False
        if self.pk is None:
            first = True
        if first:
            user = User.objects.create_user(
                username=self.cnpj,
                email=self.cnpj + '@hotel.com',
                password=self.senha)
            usuario = Usuario(usuario=user, tipo=2)
            usuario.save()
            self.usuario = usuario
            Token.objects.create(user=user)
        super().save(*args, **kwargs)


class Promocao(models.Model):
    site = models.ForeignKey(SiteReserva, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    preco = models.IntegerField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()

    def __str__(self):
        return f"{self.site} - {self.hotel}"

    class Meta:
        verbose_name_plural = "Promoção"
        verbose_name = "Promoções"

    def save(self, *args, **kwargs):
        promocoes = Promocao.objects.filter(hotel=self.hotel)
        if self.data_fim <= self.data_inicio:
            raise APIException({"msg": "Data da promoção inválida"})
        for p in promocoes:
            # (t1start <= t2start <= t1end) or (t2start <= t1start <= t2end)
            if (self.data_inicio <= p.data_inicio <= self.data_fim) or (p.data_inicio <= self.data_inicio <= p.data_fim):
                raise APIException({"msg": "Data da promoção coincíde com promoções anteriores"})
        super().save(*args, **kwargs)
