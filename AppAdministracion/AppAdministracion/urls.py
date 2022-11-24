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
    path('agregarUsuarios', views.irAgregarUsuarios),
    path('eliminarUsuarios', views.irEliminarUsuarios),
    path('agregarVehiculos', views.irAgregarVehiculos),
    # Funciones de listado
    path('listarUsuarios', views.irListarUsuarios),
    path('listarVehiculos', views.irListarVehiculos),
    # Funciones de formulario de
    path('fx_iniciarSesion', views.fxInicioSesion),
    path('fx_agregarUsuario', views.fxAgregarUsuario),
    path('fx_eliminarUsuario', views.fxEliminarUsuario),
    path('fx_agregarVehiculo', views.fxAgregarVehiculo),
    
]
