
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Unidad


@login_required
def lista_unidades(request):
    busqueda = request.GET.get("buscar", "").strip()

    unidades = (
        Unidad.objects
        .filter(activo=True)
        .select_related("unidad_de_negocio", "alcance")
    )

    if busqueda:
        unidades = unidades.filter(
            Q(dominio__icontains=busqueda)
            | Q(movil__icontains=busqueda)
        )

    unidades = unidades.order_by("id_interno")

    return render(
        request,
        "unidades/lista.html",
        {
            "unidades": unidades,
            "busqueda": busqueda,
        },
    )


@login_required
def detalle_unidad(request, pk):
    unidad = get_object_or_404(
        Unidad.objects.select_related(
            "unidad_de_negocio",
            "alcance",
        ),
        pk=pk,
    )

    return render(
        request,
        "unidades/detalle.html",
        {"unidad": unidad},
    )