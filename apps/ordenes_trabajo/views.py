from django.db.models import Q
from django.shortcuts import render

from .models import DetalleOrdenTrabajo, OrdenTrabajo


def inicio(request):
    ordenes = OrdenTrabajo.objects.all()

    busqueda = request.GET.get("buscar", "").strip()
    estado = request.GET.get("estado", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    fecha_desde = request.GET.get("fecha_desde", "").strip()
    fecha_hasta = request.GET.get("fecha_hasta", "").strip()

    if busqueda:
        ordenes = ordenes.filter(
            Q(movil__icontains=busqueda)
            | Q(dominio__icontains=busqueda)
            | Q(id__icontains=busqueda)
        )

    if estado == "abierta":
        ordenes = ordenes.filter(fecha_egreso__isnull=True)

    elif estado == "cerrada":
        ordenes = ordenes.filter(fecha_egreso__isnull=False)

    if tipo == "preventivo":
        ordenes = ordenes.filter(
            detalles__tipo=DetalleOrdenTrabajo.Tipo.PREVENTIVO
        ).distinct()

    elif tipo == "correctivo":
        ordenes = ordenes.filter(
            detalles__tipo=DetalleOrdenTrabajo.Tipo.CORRECTIVO
        ).distinct()

    if fecha_desde:
        ordenes = ordenes.filter(fecha_ingreso__gte=fecha_desde)

    if fecha_hasta:
        ordenes = ordenes.filter(fecha_ingreso__lte=fecha_hasta)

    return render(
        request,
        "ordenes_trabajo/lista.html",
        {
            "ordenes": ordenes,
            "busqueda": busqueda,
            "estado": estado,
            "tipo": tipo,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
        },
    )