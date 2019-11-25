from rest_framework import serializers
from tresvago.tresvago.models import Hotel, SiteReserva, Promocao, Usuario
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email']

    validate_password = make_password


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['usuario', 'tipo']


class HotelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'nome', 'cidade', 'cnpj', 'senha']


class SiteReservaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SiteReserva
        fields = ['id', 'nome', 'telefone', 'url', 'senha']


class PromocaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promocao
        fields = ['site', 'hotel', 'preco', 'data_inicio', 'data_fim']
        depth = 1
