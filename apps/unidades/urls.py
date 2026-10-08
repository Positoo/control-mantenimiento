from django.urls import path

from . import views


urlpatterns = [
    path("", views.lista_unidades, name="lista_unidades"),
    path("<int:pk>/", views.detalle_unidad, name="detalle_unidad"),
]