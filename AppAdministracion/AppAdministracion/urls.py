"""AppAdministracion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.irInicio),
    path('iniciarSesion', views.irInicioSesion),
    #Crud de usuaro
    path('agregarUsuarios', views.irAgregarUsuario),
    path('eliminarUsuarios', views.irEliminarUsuario),
    path('actualizarUsuarios', views.irActualizarUsuario),
    path('listarUsuarios', views.irListarUsuarios),
    path('fx_agregarUsuario', views.fxAgregarUsuario),
    path('fx_eliminarUsuario', views.fxEliminarUsuario),
    path('fx_ActualizarUsuario', views.fx_ActualizarUsuario),
    #Crud de vehiculo
    path('fx_agregarVehiculo', views.fxAgregarVehiculo),
    path('fx_ActualizarVehiculo', views.fx_ActualizarVehiculo),
    path('fxActualizarVehiculo', views.fxActualizarVehiculo),
    path('agregarVehiculos', views.irAgregarVehiculos),
    path('eliminarVehiculos', views.irEliminarVehiculos),
    path('actualizarVehiculos', views.irActualizarVehiculos),
    path('fx_iniciarSesion', views.fxInicioSesion),
    path('listarVehiculos', views.irListarVehiculos),
    path('listarRevision', views.irListarRevision),
    path('fx_eliminarVehiculo', views.fxEliminarVehiculo),
    path('buscarVehiculo', views.irBuscarVehiculos),
    path('fxBuscarVehiculo', views.fxBuscarVehiculo),
    path('buscarMarcaModelo', views.irBuscarMarcaModelo),
    #Crud de Computacion
    path('agregarComputacion',views.agregarComputacion),
    path('listarInsumos',views.listarInsumos),
    path('actualizarInsumo',views.actualizarInsumo),
    path('eliminarInsumo',views.eliminarInsumo),
    path('buscarInsumo',views.buscarInsumo),
    path('fx_BuscarMarcaModelo',views.fx_BuscarMarcaModelo),
    #Crud de oficina
    path('agregarOficina',views.agregarOficina),
    path('listarOficina',views.listarOficina),
    path('actualizarOficina',views.actualizarOficina),
    path('eliminarOficina',views.eliminarOficina),
    path('buscarOficina',views.buscarOficina)

]
