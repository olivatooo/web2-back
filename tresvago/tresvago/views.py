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


class UserViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HotelViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Hotel.objects.all().defer('senha')
    serializer_class = HotelSerializer


class SiteReservaViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = SiteReserva.objects.all().defer('senha')
    serializer_class = SiteReservaSerializer


class PromocaoViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Promocao.objects.all()
    serializer_class = PromocaoSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def test_view(request, format=None):
    try:
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    except:
        return Response({"error": "user don't have a token"})
