from django.shortcuts import render, redirect
from .models import Vehiculo, InsumoComputacional, ArticuloOficina, Usuario
from msilib.schema import Error

def irInicioSesion(request):
    try:
        if request.session['sesion_activa'] == 0 or request.session['sesion_activa'] == 1 or request.session['sesion_activa'] == 2 or request.session['sesion_activa'] ==3 :
            del request.session['sesion_activa']
            return render(request,"index.html")
        else:
            return render(request,"iniciarSesion.html")
    except:
        return render(request,"iniciarSesion.html")

def irInicio(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        if sesion != 0 and sesion != 1 and sesion != 2 and sesion != 3:
            sesion = None
    except:
        sesion = None
    return render(request,"index.html",{'sesion_activa':sesion})

def irListarUsuarios(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    us = Usuario.objects.all()
    return render(request,"listarUsuarios.html",{'sesion_activa':sesion, "usuarios":us})

def irAgregarUsuarios(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    return render(request,"agregarUsuario.html",{'sesion_activa':sesion})

def fxInicioSesion(request):
    usr = None
    try:
        usr = Usuario.objects.get(username = request.POST["form_username"])
        if (usr.password == request.POST["form_password"]):
            request.session['sesion_activa'] = usr.perfil
            return redirect(irInicio)
        else:
            return render(request,"iniciarSesion.html"), {"mensaje":"contraseña no válida"}
    except Exception as ex:
        return render(request,"iniciarSesion.html",{"mensaje":ex})

def fxAgregarUsuario(request):
    mensaje = None
    us_username = request.POST['f_username']
    us_password = request.POST['f_password']
    us_email = request.POST['f_email']
    us_nombre = request.POST['f_nombre']
    us_perfil = request.POST['f_perfil']

    try:
        Usuario.objects.create(username=us_username, password=us_password, email=us_email, nombre=us_nombre, perfil = us_perfil)
        mensaje = f"Se ha regitrado el usuario, {us_username}"
    except Exception as ex:
        if str(ex.__cause__).find('AppAdministracion_usuario.username') > 0:
            mensaje = 'El nick ya se encuentra en uso'
        elif str(ex.__cause__).find('AppAdministracion_usuario.email') > 0:
            mensaje = 'El correo ya se encuentra en uso'
        else:
            mensaje = 'Ha ocurrido un error en la operación'
    except Error as err:
        mensaje = f'ha ocurrido un problema en la operación_, {err}'
    return render(request,"respuesta.html",{'mensaje':mensaje})
