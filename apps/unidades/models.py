from django.db import models

#Unidad de Negocio puede ser Hormax en distintas ciudades y luego Alcance seria si es distribucion, producion, corralon, etc
class UnidadDeNegocio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


#Alcance. puede ser H-distribucion, H-Produccion, Corralon, etc.
class Alcance(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


#Unidades este es el modelo para crear las distintas unidades
class Unidad(models.Model):
    id_interno = models.AutoField(primary_key=True)
    movil = models.CharField(max_length=20, unique=True, blank=True)
    dominio = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=100, blank=True)
    modelo = models.CharField(max_length=100, blank=True)
    nro_chasis = models.CharField(max_length=100, blank=True)
    nro_motor = models.CharField(max_length=100, blank=True)

    capacidad_m3 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    capacidad_tn = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    unidad_de_negocio = models.ForeignKey(
        UnidadDeNegocio,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    alcance = models.ForeignKey(
        Alcance,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    observaciones = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.id_interno} - {self.dominio}"   #aqui agregar self.movil cuando tengamos definido por movil