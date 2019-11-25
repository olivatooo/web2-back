from django.contrib import admin
from .models import Hotel, Promocao, SiteReserva, Usuario

# Register your models here.
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    fields = ('usuario', 'cnpj', 'cidade')


@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    fields = ('site', 'hotel', 'data_inicio', 'data_fim', 'preco')


@admin.register(SiteReserva)
class SiteReservaAdmin(admin.ModelAdmin):
    fields = ('usuario', 'telefone', 'url')


@admin.register(Usuario)
class SiteReservaAdmin(admin.ModelAdmin):
    fields = ('usuario', 'tipo')
