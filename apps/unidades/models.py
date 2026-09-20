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