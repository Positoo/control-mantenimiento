from django.contrib import admin

from .models import UnidadDeNegocio, Alcance, Unidad


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


@admin.register(Unidad)
class UnidadAdmin(admin.ModelAdmin):
    list_display = (
        "id_interno",
        "movil",
        "dominio",
        "marca",
        "modelo",
        "unidad_de_negocio",
        "alcance",
    )

    search_fields = (
        "movil",
        "dominio",
        "marca",
        "modelo",
    )

    list_filter = (
        "unidad_de_negocio",
        "alcance",
        "activo",
    )