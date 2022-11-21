from django.shortcuts import render, redirect
from .models import Vehiculo, InsumoComputacional, ArticuloOficina, Usuario
from msilib.schema import Error

def iniciar_sesion(request):
    try:
        if request.session['sesion_activa'] == 'Activa':
            del request.session['sesion_activa']
            return render(request,"index.html")
        else:
            return render(request,"iniciar_sesion.html")
    except:
        return render(request,"iniciar_sesion.html")

def inicio(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        if sesion != 0:
            sesion = None
    except:
        sesion = None
    return render(request,"index.html",{'sesion_activa':sesion})
    