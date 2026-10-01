from django.urls import path

from . import views


urlpatterns = [
    path("", views.inicio, name="inicio"),
    path(
        "ot/nueva/",
        views.nueva_ot,
        name="nueva_ot",
    ),
    path(
        "ot/<int:pk>/",
        views.detalle_ot,
        name="detalle_ot",
    ),
    path(
        "api/buscar-unidad/",
        views.buscar_unidad,
        name="buscar_unidad",
    ),
    path("reportes/costos/", views.reporte_costos, name="reporte_costos"),
    path(
    "reportes/costos/exportar/",
    views.exportar_costos_excel,
    name="exportar_costos_excel",
    ),
]