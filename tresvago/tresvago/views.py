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
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class HotelAPIView(generics.ListCreateAPIView):
    def perform_create(self, serializer):
        print(self.request)


class SiteReservaViewSet(viewsets.ModelViewSet):
    queryset = SiteReserva.objects.all()
    serializer_class = SiteReservaSerializer


class PromocaoViewSet(viewsets.ModelViewSet):
    queryset = Promocao.objects.all()
    serializer_class = PromocaoSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def test_view(request, format=None):
    content = {
        'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        'auth': unicode(request.auth),  # None
    }
    return Response(content)
