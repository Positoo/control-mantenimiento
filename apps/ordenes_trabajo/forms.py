from django import forms
from django.forms import inlineformset_factory
from apps.unidades.models import Unidad

from .models import DetalleOrdenTrabajo, OrdenTrabajo


class OrdenTrabajoForm(forms.ModelForm):
    unidad_busqueda = forms.CharField(
        label="Dominio o Móvil",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese dominio o móvil",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = OrdenTrabajo
        fields = [
            "unidad_busqueda",
            "fecha_ingreso",
            "kilometros",
            "horas",
            "fecha_egreso",
            "observaciones",
        ]

        widgets = {
            "fecha_ingreso": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "kilometros": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "horas": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "fecha_egreso": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

    def clean_unidad_busqueda(self):
        valor = self.cleaned_data["unidad_busqueda"].strip()

        unidades = Unidad.objects.filter(
            activo=True
        ).filter(
            dominio__iexact=valor
        )

        if not unidades.exists():
            unidades = Unidad.objects.filter(
                activo=True,
                movil__iexact=valor,
            )

        if not unidades.exists():
            raise forms.ValidationError(
                "No existe una unidad activa con ese dominio o móvil."
            )

        if unidades.count() > 1:
            raise forms.ValidationError(
                "Hay más de una unidad que coincide con ese dominio o móvil."
            )

        return unidades.first()


class DetalleOrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = DetalleOrdenTrabajo
        fields = [
            "tipo",
            "observaciones",
            "cantidad",
            "costo_unitario",
            "proveedor",
            "tipo_de_comprobante",
            "numero_de_comprobante",
        ]

        widgets = {
            "tipo": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "observaciones": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "cantidad": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "costo_unitario": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "proveedor": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "tipo_de_comprobante": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "numero_de_comprobante": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


DetalleOrdenTrabajoFormSet = inlineformset_factory(
    OrdenTrabajo,
    DetalleOrdenTrabajo,
    form=DetalleOrdenTrabajoForm,
    extra=1,
    can_delete=True,
)