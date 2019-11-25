from django.shortcuts import render
from rest_framework import viewsets
from .serializers import HotelSerializer, SiteReservaSerializer, PromocaoSerializer, UserSerializer
from .models import *
from django.contrib.auth.models import User, Group
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HotelViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Hotel.objects.defer('senha')
    serializer_class = HotelSerializer


class SiteReservaViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = SiteReserva.objects.defer('senha')
    serializer_class = SiteReservaSerializer


class PromocaoViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Promocao.objects.all()
    serializer_class = PromocaoSerializer


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        usuario = Usuario.objects.get(usuario=user)
        if usuario.tipo == 1:
            site = SiteReserva.objects.get(usuario=usuario)
            return Response({
                'id': user.id,
                'tipo': usuario.tipo,
                'nome': site.nome,
                'telefone': site.telefone,
                'url': site.url,
                'token': token.key,
            })
        if usuario.tipo == 2:
            hotel = Hotel.objects.get(usuario=usuario)
            return Response({
                'id': user.id,
                'tipo': usuario.tipo,
                'nome': hotel.nome,
                'cnpj': hotel.cnpj,
                'cidade': hotel.cidade,
                'token': token.key,
            })
        return Response({"nome": str(user) , "tipo":0})


class test_auth(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here

    def get(self, request):
        user = request.user
        usuario = Usuario.objects.get(usuario=user)
        token, created = Token.objects.get_or_create(user=user)

        if usuario.tipo == 1:
            site = SiteReserva.objects.get(usuario=usuario)
            return Response({
                'id': user.id,
                'tipo': usuario.tipo,
                'nome': site.nome,
                'telefone': site.telefone,
                'url': site.url,
                'token': token.key,
            })
        if usuario.tipo == 2:
            hotel = Hotel.objects.get(usuario=usuario)
            return Response({
                'id': user.id,
                'tipo': usuario.tipo,
                'nome': hotel.nome,
                'cnpj': hotel.cnpj,
                'cidade': hotel.cidade,
                'token': token.key,
            })
        return Response({"nome": "admin", "tipo" : 0})
