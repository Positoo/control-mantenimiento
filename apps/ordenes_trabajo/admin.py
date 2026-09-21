from django.contrib import admin
from django import forms

from .models import DetalleOrdenTrabajo, OrdenTrabajo

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = "__all__"

    def save(self, commit=True):
        instancia = super().save(commit=False)

        if instancia.unidad:
            instancia.movil = instancia.unidad.movil
            instancia.dominio = instancia.unidad.dominio

        if commit:
            instancia.save()

        return instancia

class DetalleOrdenTrabajoInline(admin.TabularInline):
    model = DetalleOrdenTrabajo
    extra = 1

def formato_costo(valor):
    return f"$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(admin.ModelAdmin):

    form = OrdenTrabajoForm

    readonly_fields = (
    "movil",
    "dominio",
    "dias_detenido",
    "costo_preventivo",
    "costo_correctivo",
    "costo_total",
    )

    list_display = (
        "mostrar_numero_ot",
        "unidad",
        "movil",
        "dominio",
        "fecha_ingreso",
        "fecha_egreso",
        "dias_detenido",
        "mostrar_costo_preventivo",
        "mostrar_costo_correctivo",
        "mostrar_costo_total",
        "activa",
    )

    @admin.display(description="Costo preventivo")
    def mostrar_costo_preventivo(self, obj):
        return formato_costo(obj.costo_preventivo)

    @admin.display(description="Costo correctivo")
    def mostrar_costo_correctivo(self, obj):
        return formato_costo(obj.costo_correctivo)

    @admin.display(description="Costo total")
    def mostrar_costo_total(self, obj):
        return formato_costo(obj.costo_total)

    @admin.display(description="OT")
    def mostrar_numero_ot(self, obj):
        return obj.numero_ot

    list_filter = (
        "activa",
        "fecha_ingreso",
        "fecha_egreso",
    )

    search_fields = (
        "movil",
        "dominio",
        "unidad__movil",
        "unidad__dominio",
    )

    inlines = [DetalleOrdenTrabajoInline]


@admin.register(DetalleOrdenTrabajo)
class DetalleOrdenTrabajoAdmin(admin.ModelAdmin):
    list_display = (
        "orden_trabajo",
        "tipo",
        "observaciones",
        "cantidad",
        "costo_unitario",
        "costo_total",
        "proveedor",
        "tipo_de_comprobante",
        "numero_de_comprobante",
    )

    list_filter = (
        "tipo",
        "tipo_de_comprobante",
    )

    search_fields = (
        "observaciones",
        "proveedor",
        "numero_de_comprobante",
    )