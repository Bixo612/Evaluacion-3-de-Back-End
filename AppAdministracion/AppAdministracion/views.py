from django.shortcuts import render, redirect
from .models import Vehiculo, InsumoComputacional, ArticuloOficina, Usuario
from msilib.schema import Error
from inspect import ArgSpec

# Funciones de redirecion

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



def irAgregarUsuarios(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    return render(request,"agregarUsuario.html",{'sesion_activa':sesion})

def irEliminarUsuarios(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    if sesion == 0:
        return render(request,"eliminarUsuario.html",{'sesion_activa':sesion})
    else:
        return render(request,"index.html",{'sesion_activa':sesion})

def irAgregarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    return render(request,"agregarVehiculo.html",{'sesion_activa':sesion})

# Funciones de interacion

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

def fxAgregarVehiculo(request):
    mensaje = None
    ve_patente = request.POST['f_patente']
    ve_numero_chasis = request.POST['f_numero_chasis']
    ve_marca = request.POST['f_marca']
    ve_modelo = request.POST['f_modelo']
    ve_ultima_revision = request.POST['f_ultima_revision']
    ve_proxima_revision = request.POST['f_proxima_revision']
    ve_observaciones = request.POST['f_observaciones']

    try:
        Vehiculo.objects.create(
            patente = ve_patente, 
            numero_chasis = ve_numero_chasis, 
            marca = ve_marca, 
            modelo = ve_modelo, 
            ultima_revision = ve_ultima_revision, 
            proxima_revision = ve_proxima_revision, 
            observaciones = ve_observaciones)
        mensaje = f"Se ha regitrado el vehiculo, {ve_patente}"
    except Exception as ex:
        if str(ex.__cause__).find('AppAdministracion_vehiculo.patente') > 0:
            mensaje = 'Ya existe un registro con esa patente'
        elif str(ex.__cause__).find('AppAdministracion_usuario.numero_chasis') > 0:
            mensaje = 'Ya existe un registro con ese numero de chasis'
        else:
            mensaje = 'Ha ocurrido un error en la operación'
    except Error as err:
        mensaje = f'ha ocurrido un problema en la operación_, {err}'
    return render(request,"respuesta.html",{'mensaje':mensaje})

def fxEliminarUsuario(request):
    mensaje = None
    try:
        usr = Usuario.objects.get(username = request.GET["f_username"])
        usr.delete()
        mensaje = "Persona eliminada"
        return render(request, 'eliminar.html',{'mensaje':mensaje})
    except Exception as ex:
        if str(ex.args).find('does not exist') > 0:
            mensaje = 'Usuario no exite'
        else:
            mensaje = 'Ha ocurrido un problema'        
        return render(request,"eliminarUsuario.html", {'mensaje':mensaje})

# Listar

def irListarUsuarios(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    us = Usuario.objects.all()
    return render(request,"listarUsuarios.html",{'sesion_activa':sesion, "usuarios":us})

def irListarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    ve = Vehiculo.objects.all()
    return render(request,"listarVehiculos.html",{'sesion_activa':sesion, "vehiculos":ve})