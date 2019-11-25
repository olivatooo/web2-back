from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.dateparse import parse_datetime


from .models import *
from .serializers import HotelSerializer, SiteReservaSerializer, PromocaoSerializer, UserSerializer


def has_permission(permission, user):
    if user.tipo == permission:
        return True
    return False


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


class PromocaoFilter(APIView):
    def get(self, request):
        promocoes = Promocao.objects.all()
        data = request.GET
        if 'site' in data:
            promocoes = promocoes.filter(site=data['site'])
        if 'hotel' in data:
            promocoes = promocoes.filter(hotel=data['hotel'])
        if 'cidade' in data:
            promocoes = promocoes.filter(hotel__cidade=data['cidade'])
        if 'data_inicio' in data:
            inicio = parse_datetime(data['data_inicio'])
            promocoes = promocoes.filter(data_inicio__gte=inicio)
        if 'data_fim' in data:
            fim = parse_datetime(data['data_fim'])
            promocoes = promocoes.filter(data_fim__lte=fim)

        return Response(PromocaoSerializer(promocoes, many=True).data)


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
                'id': site.id,
                'tipo': usuario.tipo,
                'nome': site.nome,
                'telefone': site.telefone,
                'url': site.url,
                'token': token.key,
            })
        if usuario.tipo == 2:
            hotel = Hotel.objects.get(usuario=usuario)
            return Response({
                'id': hotel.id,
                'tipo': usuario.tipo,
                'nome': hotel.nome,
                'cnpj': hotel.cnpj,
                'cidade': hotel.cidade,
                'token': token.key,
            })

        return Response({"nome": str(user), "tipo": 0, 'token': token.key})


class TestAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        usuario = Usuario.objects.get(usuario=user)
        token, created = Token.objects.get_or_create(user=user)

        if usuario.tipo == 1:
            site = SiteReserva.objects.get(usuario=usuario)
            return Response({
                'id': site.id,
                'tipo': usuario.tipo,
                'nome': site.nome,
                'telefone': site.telefone,
                'url': site.url,
                'token': token.key,
            })
        if usuario.tipo == 2:
            hotel = Hotel.objects.get(usuario=usuario)
            return Response({
                'id': hotel.id,
                'tipo': usuario.tipo,
                'nome': hotel.nome,
                'cnpj': hotel.cnpj,
                'cidade': hotel.cidade,
                'token': token.key,
            })
        return Response({"nome": "admin", "tipo": 0, "token": token.key})
