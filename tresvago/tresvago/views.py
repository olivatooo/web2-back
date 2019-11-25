from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def list(self, request, **kwargs):
        try:
            fields = Hotel._meta.fields
            fields.remove('senha')
            queryset = Hotel.objects.defer('senha').values(*fields)
            serializer = HotelSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)


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
        data = request.data
        if 'site' in data:
            promocoes = promocoes.filter(site=data['site'])
        if 'hotel' in data:
            promocoes = promocoes.filter(hotel=data['hotel'])
        if 'cidade' in data:
            promocoes = promocoes.filter(cidade=data['cidade'])
        if 'data_inicio' in data and 'data_fim' in data:
            promocoes = promocoes.filter(data_inicio__gte=data['data_inicio'])
            promocoes = promocoes.filter(data_fim__lte=data['data_fim'])

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

        return Response({"nome": str(user), "tipo": 0, 'token': token.key})


class TestAuth(APIView):
    permission_classes = (IsAuthenticated,)  # <-- And here

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
        return Response({"nome": "admin", "tipo": 0, "token": token.key})
