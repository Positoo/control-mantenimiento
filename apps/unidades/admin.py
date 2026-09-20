from django.contrib import admin

from .models import UnidadDeNegocio, Alcance


@admin.register(UnidadDeNegocio)
class UnidadDeNegocioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)

@admin.register(Alcance)
class AlcanceAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre",)