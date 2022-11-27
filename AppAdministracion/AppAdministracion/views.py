from django.shortcuts import render, redirect
from .models import Vehiculo, InsumoComputacional, ArticuloOficina, Usuario
from msilib.schema import Error
from inspect import ArgSpec
from django.contrib.auth.decorators import login_required

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

def irAgregarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    return render(request,"agregarVehiculo.html",{'sesion_activa':sesion})

def irInicio(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        if sesion != 0 and sesion != 1 and sesion != 2 and sesion != 3:
            sesion = None
    except:
        sesion = None
    return render(request,"index.html",{'sesion_activa':sesion})

# Redireciones de crud de usuarios

def irAgregarUsuario(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    return render(request,"agregarUsuario.html",{'sesion_activa':sesion})

def irEliminarUsuario(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    if sesion == 0:
        return render(request,"eliminarUsuario.html",{'sesion_activa':sesion})
    else:
        return render(request,"index.html",{'sesion_activa':sesion})

def irActualizarUsuario(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    if sesion == 0:
        return render(request,"actualizarUsuario.html",{'sesion_activa':sesion})
    else:
        return render(request,"index.html",{'sesion_activa':sesion})



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

def fx_ActualizarUsuario(request):
    usr = None
    mensaje = None
    try:
        usr = Usuario.objects.get(username = request.GET["ff_username"])
        return render(request,'ActualizarUsuario.html',{"usr":usr})
    except:
        usr = None

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
        Vehiculo.objects.create(patente = ve_patente, numero_chasis = ve_numero_chasis, marca = ve_marca, modelo = ve_modelo, ultima_revision = ve_ultima_revision, proxima_revision = ve_proxima_revision, observaciones = ve_observaciones)
        mensaje = f"Se ha regitrado el vehiculo {ve_patente} / {ve_marca} / {ve_modelo}"
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


#Funciones CRUD Computacion

def agregarComputacion(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    try:
        mensaje = ""
        numero_insumo = request.POST['f_numero_insumo']
        nombre = request.POST['f_nombre']
        fecha_adquisicion = request.POST['f_fecha_adquisicion']
        marca = request.POST['f_marca']
        stock = request.POST['f_stock']
        descripcion = request.POST['f_descripcion']
        InsumoComputacional.objects.create(numero_insumo = numero_insumo,nombre=nombre, fecha_adquisicion=fecha_adquisicion, marca=marca, stock=stock, descripcion = descripcion)
        mensaje = f"Se ha regitrado el Insumo computacional {numero_insumo} / {nombre} / {fecha_adquisicion}"
    except Exception as ex:
        if str(ex.__cause__).find('AppAdministracion_insumocomputacional.numero_insumo') > 0:
            mensaje = 'Ya existe un registro con ese numero de insumo'
    except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
    except:
        return render(request,"agregarComputacion/agregarComputacion.html",{'mensaje':mensaje,"sesion_activa":sesion})
    return render(request,"agregarComputacion/agregarComputacion.html",{'mensaje':mensaje,"sesion_activa":sesion})  


def listarInsumos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    insumo = InsumoComputacional.objects.all()
    return render(request,"agregarComputacion/listarInsumos.html",{"insumo":insumo,"sesion_activa":sesion})


def eliminarInsumo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    mensaje = None
    try:
        usr = InsumoComputacional.objects.get(numero_insumo = request.GET["numero_insumo"])
        usr.delete()
        mensaje = "Insumo eliminado"
        return render(request, 'agregarComputacion/eliminarInsumo.html',{'mensaje':mensaje,"sesion_activa":sesion})
    except Exception as ex:
        if str(ex.args).find('does not exist') > 0:
            mensaje = 'Insumo no exite'
        else:
            mensaje = 'Ha ocurrido un problema'        
        return render(request,"agregarComputacion/eliminarInsumo.html",{mensaje:'mensaje',"sesion_activa":sesion})

def actualizarInsumo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    usr = None
    msj = None
    try:
        usr = InsumoComputacional.objects.get(numero_insumo = request.GET["nInsumo"])
        return render(request, "agregarComputacion/actualizarInsumo.html",{"usr":usr,"sesion_activa":sesion})
    except:
        usr = None
    
    if usr == None:
        numero_insumo = None
        try:
            numero_insumo = request.POST["f_numero_insumo"]
        except:
            numero_insumo = None

        if numero_insumo != None:
            usr = InsumoComputacional.objects.get(numero_insumo = numero_insumo)
            nombre = request.POST['f_nombre']
            fecha_adquisicion = request.POST['f_fecha_adquisicion']
            marca = request.POST['f_marca']
            stock = request.POST['f_stock']
            descripcion = request.POST['f_descripcion']

            usr.nombre = nombre
            usr.fecha_adquisicion = fecha_adquisicion
            usr.marca = marca
            usr.stock = stock
            usr.descripcion = descripcion
            try:
                usr.save()
                msj = "Se ha actualizado el insumo"
            except:
                msj = f"ha ocurrido un error al actualizar el insumo"
            return render(request, "agregarComputacion/actualizarInsumo.html", {"msj":msj,"sesion_activa":sesion})
        else:
            msj = "No se ha encontrado el insumo"
            return render(request, "agregarComputacion/actualizarInsumo.html", {"msj":msj,"sesion_activa":sesion})
    else:
        msj = "No se encontró el insumo solicitado"
        return render(request, "agregarComputacion/actualizarInsumo.html", {"msj":msj,"sesion_activa":sesion})

def buscarInsumo(request):
    sesion = None
    datos = None
    visibilidad = "Hidden"
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request,"iniciarSesion.html")
    try:
        mensaje = ""
        for i in request.GET["buscarInsumo"]:
            if (i== chr(48) or i== chr(49) or i == chr(50) or
             i == chr(51) or 
             i == chr(52) or i == chr(53) or i == chr(54) or 
             i == chr(55) or i == chr(56) or i == chr(57)):
                  mensaje = "Ingreso numero"
            else:
                mensaje = "Ingreso letra"
                break

        if mensaje=="Ingreso numero":
            datos = InsumoComputacional.objects.get(numero_insumo = request.GET["buscarInsumo"])
            visibilidad = "visible"
            mensaje="Insumo buscado por numero"

        elif mensaje=="Ingreso letra":
            datos = InsumoComputacional.objects.get(nombre = request.GET["buscarInsumo"])
            visibilidad = "visible"
            mensaje="Insumo buscado por nombre"

        return render(request, 'agregarComputacion/buscarInsumo.html',{'mensaje':mensaje,"sesion_activa":sesion,"ins":datos,"visibilidad":visibilidad})
    except Exception as ex:
                  mensaje = 'Error en la matrix'  
    return render(request,"agregarComputacion/buscarInsumo.html",{mensaje:'mensaje',"sesion_activa":sesion,"visibilidad":visibilidad})