from django.shortcuts import render, redirect
from .models import Vehiculo, InsumoComputacional, ArticuloOficina, Usuario
from msilib.schema import Error

def irInicioSesion(request):
    try:
        if request.session['sesion_activa'] == 0:
            del request.session['sesion_activa']
            return render(request,"index.html")
        else:
            return render(request,"iniciarSesion.html")
    except:
        return render(request,"iniciarSesion.html")

def fxInicioSesion(request):
    usr = None
    try:
        usr = Usuario.objects.get(username = request.POST["form_username"])
        if (usr.password == request.POST["form_password"]):
            request.session['sesion_activa'] = 0
            return redirect(irInicio)
        else:
            return render(request,"iniciarSesion.html"), {"mensaje":"contraseña no válida"}
    except Exception as ex:
        return render(request,"iniciarSesion.html",{"mensaje":ex})

# def sesion(request):
#     per = None
#     try:
#         per = Persona.objects.get(rut = request.POST["rut"])
#         if(per.contrasenna == request.POST["contrasenna"]):
#             request.session["sesion_activa"] = "Activa"
#             return redirect(inicio)
#         else:
#             return render(request,"iniciar_sesion.html", {"mensaje":"contraseña no válida"})
#     except Exception as ex:
#         return render(request,"iniciar_sesion.html", {"mensaje":ex})


def irInicio(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        if sesion != 0:
            sesion = None
    except:
        sesion = None
    return render(request,"index.html",{'sesion_activa':sesion})

def irRespuesta(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciar_sesion.html")
    return render(request,"respuesta.html",{'sesion_activa':sesion})
    