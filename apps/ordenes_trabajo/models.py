from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class OrdenTrabajo(models.Model):
    unidad = models.ForeignKey(
        "unidades.Unidad",
        on_delete=models.PROTECT,
        related_name="ordenes_trabajo",
    )

    movil = models.CharField(max_length=20, blank=True)
    dominio = models.CharField(max_length=20)

    fecha_ingreso = models.DateField()
    kilometros = models.PositiveIntegerField(null=True, blank=True)
    horas = models.PositiveIntegerField(null=True, blank=True)
    fecha_egreso = models.DateField(null=True, blank=True)

    observaciones = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"OT-{self.id:06d}"

    @property
    def numero_ot(self):
        return f"OT-{self.id:06d}"

    @property
    def dias_detenido(self):
        if self.fecha_egreso is None:
            return None

        return (self.fecha_egreso - self.fecha_ingreso).days

    @property
    def costo_preventivo(self):
        return sum(
        detalle.costo_total
        for detalle in self.detalles.filter(
            tipo=DetalleOrdenTrabajo.Tipo.PREVENTIVO
        )
        )

    @property
    def costo_correctivo(self):
        return sum(
            detalle.costo_total
            for detalle in self.detalles.filter(
                tipo=DetalleOrdenTrabajo.Tipo.CORRECTIVO
            )
        )

    @property
    def costo_total(self):
        return self.costo_preventivo + self.costo_correctivo

    def clean(self):
        if (
            self.fecha_egreso is not None
            and self.fecha_egreso < self.fecha_ingreso
        ):
            raise ValidationError(
                "La fecha de egreso no puede ser anterior a la fecha de ingreso."
            )


class DetalleOrdenTrabajo(models.Model):
    class Tipo(models.TextChoices):
        PREVENTIVO = "PREVENTIVO", "Preventivo"
        CORRECTIVO = "CORRECTIVO", "Correctivo"

    class TipoComprobante(models.TextChoices):
        FACTURA = "FACTURA", "Factura"
        REMITO = "REMITO", "Remito"
        SIN_COMPROBANTE = "SIN_COMPROBANTE", "Sin comprobante"
        OTRO = "OTRO", "Otro"

    orden_trabajo = models.ForeignKey(
        OrdenTrabajo,
        on_delete=models.PROTECT,
        related_name="detalles",
    )

    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
    )

    observaciones = models.TextField()

    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    costo_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    proveedor = models.CharField(
        max_length=100,
        blank=True,
    )

    tipo_de_comprobante = models.CharField(
        max_length=20,
        choices=TipoComprobante.choices,
    )

    numero_de_comprobante = models.CharField(
        max_length=50,
        blank=True,
    )

    @property
    def costo_total(self):
        return self.cantidad * self.costo_unitario

    def clean(self):
        if self.cantidad <= Decimal("0"):
            raise ValidationError(
                "La cantidad debe ser mayor que 0."
            )

        if self.costo_unitario < Decimal("0"):
            raise ValidationError(
                "El costo unitario no puede ser negativo."
            )

    def __str__(self):
        return f"{self.orden_trabajo} - {self.tipo}"