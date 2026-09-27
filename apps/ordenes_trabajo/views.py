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


def reporte_costos(request):
    from collections import defaultdict
    from apps.unidades.models import UnidadDeNegocio, Alcance

    ordenes = OrdenTrabajo.objects.all()

    fecha_desde = request.GET.get("fecha_desde", "").strip()
    fecha_hasta = request.GET.get("fecha_hasta", "").strip()
    unidad_negocio = request.GET.get("unidad_negocio", "").strip()
    alcance = request.GET.get("alcance", "").strip()
    movil = request.GET.get("movil", "").strip()
    tipo = request.GET.get("tipo", "").strip()

    # Filtros
    if fecha_desde:
        ordenes = ordenes.filter(fecha_ingreso__gte=fecha_desde)

    if fecha_hasta:
        ordenes = ordenes.filter(fecha_ingreso__lte=fecha_hasta)

    if unidad_negocio:
        ordenes = ordenes.filter(
            unidad_de_negocio_id=unidad_negocio
        )

    if alcance:
        ordenes = ordenes.filter(
            alcance_id=alcance
        )

    if movil:
        ordenes = ordenes.filter(
            movil__icontains=movil
        )

    if tipo == "preventivo":
        ordenes = ordenes.filter(
            detalles__tipo=DetalleOrdenTrabajo.Tipo.PREVENTIVO
        ).distinct()

    elif tipo == "correctivo":
        ordenes = ordenes.filter(
            detalles__tipo=DetalleOrdenTrabajo.Tipo.CORRECTIVO
        ).distinct()

    # Estructura:
    # Unidad de Negocio → Alcance → Unidad
    reporte = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(
                lambda: {
                    "preventivo": 0,
                    "correctivo": 0,
                    "total": 0,
                }
            )
        )
    )

    for ot in ordenes:
        detalles = ot.detalles.all()

        for detalle in detalles:
            costo = detalle.costo_total

            if detalle.tipo == DetalleOrdenTrabajo.Tipo.PREVENTIVO:
                reporte[
                    ot.unidad_de_negocio
                ][
                    ot.alcance
                ][
                    ot.unidad
                ]["preventivo"] += costo

            elif detalle.tipo == DetalleOrdenTrabajo.Tipo.CORRECTIVO:
                reporte[
                    ot.unidad_de_negocio
                ][
                    ot.alcance
                ][
                    ot.unidad
                ]["correctivo"] += costo

            reporte[
                ot.unidad_de_negocio
            ][
                ot.alcance
            ][
                ot.unidad
            ]["total"] += costo

    # Convertimos defaultdict en una estructura más cómoda para el template.
    reporte_final = []

    total_general_preventivo = 0
    total_general_correctivo = 0
    total_general = 0

    for negocio, alcances in reporte.items():

        negocio_preventivo = 0
        negocio_correctivo = 0
        negocio_total = 0

        alcances_final = []

        for alcance_obj, unidades in alcances.items():

            alcance_preventivo = 0
            alcance_correctivo = 0
            alcance_total = 0

            unidades_final = []

            for unidad, costos in unidades.items():

                unidad_total = costos["total"]

                unidades_final.append({
                    "unidad": unidad,
                    "preventivo": costos["preventivo"],
                    "correctivo": costos["correctivo"],
                    "total": unidad_total,
                })

                alcance_preventivo += costos["preventivo"]
                alcance_correctivo += costos["correctivo"]
                alcance_total += unidad_total

            alcances_final.append({
                "alcance": alcance_obj,
                "preventivo": alcance_preventivo,
                "correctivo": alcance_correctivo,
                "total": alcance_total,
                "unidades": unidades_final,
            })

            negocio_preventivo += alcance_preventivo
            negocio_correctivo += alcance_correctivo
            negocio_total += alcance_total

        reporte_final.append({
            "negocio": negocio,
            "preventivo": negocio_preventivo,
            "correctivo": negocio_correctivo,
            "total": negocio_total,
            "alcances": alcances_final,
        })

        total_general_preventivo += negocio_preventivo
        total_general_correctivo += negocio_correctivo
        total_general += negocio_total

    unidades_de_negocio = UnidadDeNegocio.objects.filter(
        activo=True
    ).order_by("nombre")

    alcances = Alcance.objects.filter(
        activo=True
    ).order_by("nombre")

    return render(
        request,
        "ordenes_trabajo/reporte_costos.html",
        {
            "reporte": reporte_final,
            "total_general_preventivo": total_general_preventivo,
            "total_general_correctivo": total_general_correctivo,
            "total_general": total_general,
            "unidades_de_negocio": unidades_de_negocio,
            "alcances": alcances,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
            "unidad_negocio": unidad_negocio,
            "alcance": alcance,
            "movil": movil,
            "tipo": tipo,
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
            ot.unidad_de_negocio = ot.unidad.unidad_de_negocio
            ot.alcance = ot.unidad.alcance

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