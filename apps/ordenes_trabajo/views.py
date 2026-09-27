from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse

from .models import DetalleOrdenTrabajo, OrdenTrabajo
from .forms import DetalleOrdenTrabajoFormSet, OrdenTrabajoForm

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


def detalle_ot(request, pk):
    ot = get_object_or_404(
        OrdenTrabajo,
        pk=pk,
    )

    return render(
        request,
        "ordenes_trabajo/detalle.html",
        {
            "ot": ot,
        },
    )

def nueva_ot(request):
    if request.method == "POST":
        form = OrdenTrabajoForm(request.POST)
        formset = DetalleOrdenTrabajoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            ot = form.save(commit=False)

            ot.unidad = form.cleaned_data["unidad_busqueda"]
            ot.movil = ot.unidad.movil or ""
            ot.dominio = ot.unidad.dominio

            ot.save()

            detalles = formset.save(commit=False)

            for detalle in detalles:
                detalle.orden_trabajo = ot
                detalle.save()

            return redirect(
                "detalle_ot",
                pk=ot.pk,
            )

    else:
        form = OrdenTrabajoForm()
        formset = DetalleOrdenTrabajoFormSet()

    return render(
        request,
        "ordenes_trabajo/nueva.html",
        {
            "form": form,
            "formset": formset,
        },
    )

def buscar_unidad(request):
    valor = request.GET.get("valor", "").strip()

    if not valor:
        return JsonResponse({
            "encontrada": False,
            "mensaje": "Ingrese un dominio o móvil.",
        })

    from apps.unidades.models import Unidad

    unidades = Unidad.objects.filter(
        activo=True
    ).filter(
        Q(dominio__iexact=valor) | Q(movil__iexact=valor)
    )

    if not unidades.exists():
        return JsonResponse({
            "encontrada": False,
            "mensaje": "No existe una unidad activa con ese dominio o móvil.",
        })

    if unidades.count() > 1:
        return JsonResponse({
            "encontrada": False,
            "mensaje": "Hay más de una unidad que coincide con ese valor.",
        })

    unidad = unidades.first()

    return JsonResponse({
        "encontrada": True,
        "id": unidad.id_interno,
        "dominio": unidad.dominio,
        "movil": unidad.movil or "",
    })