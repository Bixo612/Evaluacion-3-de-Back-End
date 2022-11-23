from django.db import models

class Vehiculo(models.Model):
    patente             = models.CharField (primary_key=True, max_length=6)
    numero_chasis       = models.CharField (unique=True, max_length=17)
    marca               = models.CharField (max_length=10)
    modelo              = models.CharField (max_length=10)
    ultima_revision     = models.DateField ()
    proxima_revision    = models.DateField ()
    observaciones       = models.CharField (max_length=200)

class InsumoComputacional(models.Model):
    numero_insumo       = models.IntegerField (primary_key=True)
    nombre              = models.CharField (max_length = 50) 
    fecha_adquisicion   = models.DateField ()
    marca               = models.CharField (max_length = 30)
    stock               = models.IntegerField ()
    descripcion         = models.CharField (max_length = 100)

class ArticuloOficina(models.Model):
    numero_articulo     = models.IntegerField (primary_key=True)
    nombre              = models.CharField (max_length = 50) 
    ubicacion           = models.CharField (max_length = 25)
    stock               = models.IntegerField ()
    descripcion         = models.CharField (max_length = 100)

class Usuario(models.Model):
    username    = models.CharField (primary_key=True, max_length = 25)
    password    = models.CharField (max_length = 40)
    email       = models.CharField (unique= True, max_length = 60)
    nombre      = models.CharField (max_length = 60)
    perfil      = models.IntegerField ()

# Usuario.objects.create (username = 'admin', password = 'adminadmin', email = 'a@admin.cl' , nombre = 'administrador general' , perfil = 0)