from django.shortcuts import render, redirect
from .models import Vehiculo, InsumoComputacional, ArticuloOficina, Usuario
from msilib.schema import Error
from inspect import ArgSpec
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import timedelta

# Funciones de redirecion

def irInicioSesion(request):
    try:
        if request.session['sesion_activa'] == 0 or request.session['sesion_activa'] == 1 or request.session['sesion_activa'] == 2 or request.session['sesion_activa'] == 3:
            del request.session['sesion_activa']
            return render(request, "index.html")
        else:
            return render(request, "iniciarSesion.html")
    except:
        return render(request, "iniciarSesion.html")

def irInicio(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        if sesion != 0 and sesion != 1 and sesion != 2 and sesion != 3:
            sesion = None
    except:
        sesion = None
    return render(request, "index.html", {'sesion_activa': sesion})

def fxInicioSesion(request):
    usr = None
    try:
        usr = Usuario.objects.get(username=request.POST["form_username"])
        if (usr.password != request.POST["form_password"]):
            return render(request, "iniciarSesion.html"), {"mensaje": "Datos incorrectos"}
        elif (usr.password == request.POST["form_password"]):
            request.session['sesion_activa'] = usr.perfil
            return redirect(irInicio)
        else:
            return render(request, "iniciarSesion.html"), {"mensaje": "Datos incorrectos"}
    except Exception as ex:
        return render(request, "iniciarSesion.html", {"mensaje": ex})

# CRUD DE USUARIOS

    # REDIRECIONES

def irAgregarUsuario(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0:
        return render(request, "crudUsuarios/agregarUsuario.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irEliminarUsuario(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0:
        return render(request, "crudUsuarios/eliminarUsuario.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irActualizarUsuario(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0:
        return render(request, "crudUsuarios/actualizarUsuario.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irListarUsuarios(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0:
        us = Usuario.objects.all()
        return render(request, "crudUsuarios/listarUsuarios.html", {'sesion_activa': sesion, "usuarios": us})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

    # FUNCIONES

def fx_ActualizarUsuario(request):
    sesion = None
    try:
        sesion = request.session["sesion_activa"]
    except:
        return render(request, "index.html", {'sesion_activa': sesion})
    if sesion == 0:
        usr = None
        msj = None
        try:
            usr = Usuario.objects.get(username=request.GET["ff_username"])
            return render(request, "crudUsuarios/actualizarUsuario.html", {"usr": usr, "sesion_activa": sesion})
        except:
            usr = None
        if usr == None:
            nick = None
            try:
                nick = request.POST["f_username"]
            except:
                nick = None

            if nick != None:
                usr = Usuario.objects.get(username=nick)
                clave = request.POST["f_password"]
                correo = request.POST["f_email"]
                nombr = request.POST["f_nombre"]
                perf = request.POST["f_perfil"]
                #
                usr.password = clave
                usr.email = correo
                usr.nombre = nombr
                usr.perfil = perf
                try:
                    usr.save()
                    msj = "Se ha actualizado el articulo de oficina"
                except:
                    msj = f"ha ocurrido un error al actualizar el usuario"
                return render(request, "crudUsuarios/actualizarUsuario.html", {"msj": msj, "sesion_activa": sesion})
            else:
                msj = "No se ha encontrado el usuario"
                return render(request, "crudUsuarios/actualizarUsuario.html", {"msj": msj, "sesion_activa": sesion})
        else:
            msj = "No se encontró el usuario solicitado"
            return render(request, "crudUsuarios/actualizarUsuario.html", {"msj": msj, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def fxAgregarUsuario(request):
    sesion = None
    try:
        sesion = request.session["sesion_activa"]
    except:
        return render(request, "index.html", {'sesion_activa': sesion})
    if sesion == 0:
        mensaje = None
        us_username = request.POST['f_username']
        us_password = request.POST['f_password']
        us_email = request.POST['f_email']
        us_nombre = request.POST['f_nombre']
        us_perfil = request.POST['f_perfil']
        try:
            Usuario.objects.create(username=us_username, password=us_password,
                                   email=us_email, nombre=us_nombre, perfil=us_perfil)
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
        return render(request, "respuesta.html", {'mensaje': mensaje,'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def fxEliminarUsuario(request):
    sesion = None
    try:
        sesion = request.session["sesion_activa"]
    except:
        return render(request, "index.html", {'sesion_activa': sesion})
    if sesion == 0:
        mensaje = None
        try:
            usr = Usuario.objects.get(username=request.GET["f_username"])
            usr.delete()
            mensaje = "Persona eliminada"
            return render(request, 'crudUsuarios/eliminarUsuario.html', {'mensaje': mensaje, 'sesion_activa': sesion})
        except Exception as ex:
            if str(ex.args).find('does not exist') > 0:
                mensaje = 'Usuario no exite'
            else:
                mensaje = 'Ha ocurrido un problema'
            return render(request, "crudUsuarios/eliminarUsuario.html", {'mensaje': mensaje, 'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

# CRUD DE VEHICULOS

    # REDIRECIONES

def irActualizarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 2:
        return render(request, "actualizarVehiculo.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irEliminarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 2:
        return render(request, "eliminarVehiculo.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irAgregarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 2:
        return render(request, "agregarVehiculo.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irBuscarVehiculos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 2:
        return render(request, "buscarVehiculo.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irBuscarMarcaModelo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 2:
        return render(request, "buscarMarcaModelo.html", {'sesion_activa': sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})


def irListarVehiculos(request):
    sesion = None
    try:
        sesion = request.session["sesion_activa"]
    except:
        return render(request, "index.html", {'sesion_activa': sesion})
    if sesion == 0 or sesion == 2:
        ve = Vehiculo.objects.all()
        return render(request, "listarVehiculos.html", {'sesion_activa': sesion, "vehiculos": ve})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def irListarRevision(request):
    sesion = None
    today = date.today()
    en1mes = today + timedelta(days=30)

    try:
        sesion = request.session["sesion_activa"]
    except:
        return render(request, "index.html", {'sesion_activa': sesion})
    if sesion == 0 or sesion == 2:
        ve = Vehiculo.objects.all()
        return render(request, "listarRevision.html", {'sesion_activa': sesion, "vehiculos": ve ,'hoy':today,'en1mes':en1mes})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

    # FUNCIONES

def fx_BuscarMarcaModelo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
        tipo_dato = request.GET["tipo_dato"]
        variable = request.GET["variable"]
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 2:
        ve = Vehiculo.objects.all()
        return render(request, "buscarMarcaModelo.html", {'sesion_activa': sesion, "vehiculos": ve, "tipo_dato": tipo_dato, "variable": variable})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def fxBuscarVehiculo(request):
    sesion = None
    bus = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    try:
        opcion = request.GET["busqueda"]
        search = request.GET["buscarVehiculo"]

        match opcion:
            case "chasis":
                bus = Vehiculo.objects.get(numero_chasis=search)
            case "patente":
                bus = Vehiculo.objects.get(patente=search)
        return render(request, "buscarVehiculo.html", {'bus': bus, 'sesion_activa': sesion})
    except Exception as ex:
        mensaje = 'ha ocurrido un error' + ex
    return render(request, "buscarVehiculo.html", {'mensaje': mensaje, 'sesion_activa': sesion})

def fx_ActualizarVehiculo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    car = None
    mensaje = None
    try:
        car = Vehiculo.objects.get(patente=request.GET["f_patente"])
        return render(request, 'actualizarVehiculo.html', {"car": car,'sesion_activa': sesion})
    except:
        mensaje = "el vehiculo no se encuentra registrado"
        return render(request, 'actualizarVehiculo.html', {"mensaje": mensaje,'sesion_activa': sesion})

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
        sesion = request.session['sesion_activa']
        Vehiculo.objects.create(patente=ve_patente, numero_chasis=ve_numero_chasis, marca=ve_marca, modelo=ve_modelo,
                                ultima_revision=ve_ultima_revision, proxima_revision=ve_proxima_revision, observaciones=ve_observaciones)
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
    return render(request, "respuesta.html", {'mensaje': mensaje, 'sesion_activa': sesion})

def fxEliminarVehiculo(request):
    mensaje = None
    try:
        sesion = request.session['sesion_activa']
        car = Vehiculo.objects.get(patente=request.GET["f_patente"])
        car.delete()
        mensaje = "Vehiculo eliminado"
        return render(request, 'eliminarVehiculo.html', {'mensaje': mensaje, 'sesion_activa': sesion})
    except Exception as ex:
        if str(ex.args).find('does not exist') > 0:
            mensaje = 'Vehículo no existe'
        else:
            mensaje = 'Ha ocurrido un problema'
        return render(request, "eliminarVehiculo.html", {'mensaje': mensaje, 'sesion_activa': sesion})

def fxActualizarVehiculo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    car = None
    mensaje = None
    oldpatente = request.POST['oldpatente']
    ve_numero_chasis = request.POST['f_chasis']
    ve_marca = request.POST['f_marca']
    ve_modelo = request.POST['f_modelo']
    ve_ultima_revision = request.POST['f_ultima_revision']
    ve_proxima_revision = request.POST['f_proxima_revision']
    ve_observaciones = request.POST['f_observaciones']

    try:
        print(oldpatente)
        car = Vehiculo.objects.get(patente=oldpatente)

        car.numero_chasis = ve_numero_chasis
        car.marca = ve_marca
        car.modelo = ve_modelo
        car.ultima_revision = ve_ultima_revision
        car.proxima_revision = ve_proxima_revision
        car.observaciones = ve_observaciones

        car.save()
        mensaje = f"Se ha actualizado el vehiculo {oldpatente} / {ve_marca} / {ve_modelo}"
        return render(request, "respuesta.html", {'mensaje': mensaje,'sesion_activa':sesion})
    except Exception as ex:
        if str(ex.__cause__).find('AppAdministracion_vehiculo.patente') > 0:
            mensaje = 'patente no existe'
        elif str(ex.__cause__).find('AppAdministracion_vehiculo.numero_chasis') > 0:
            mensaje = 'Ya existe un registro con ese numero de chasis'
        else:
            print(ex.__cause__)
            mensaje = 'Ha ocurrido un error en la operación'
    except Error as err:
        mensaje = f'ha ocurrido un problema en la operación_, {err}'
    return render(request, "respuesta.html", {'mensaje': mensaje,'sesion_activa':sesion})

# CRUD COMPUTACION

def listarInsumos(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 1:
        insumo = InsumoComputacional.objects.all()
        return render(request, "crudInsumosComputacion/listarInsumos.html", {"insumo": insumo, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def agregarComputacion(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 1:
        try:
            mensaje = ""
            numero_insumo = request.POST['f_numero_insumo']
            nombre = request.POST['f_nombre']
            fecha_adquisicion = request.POST['f_fecha_adquisicion']
            marca = request.POST['f_marca']
            stock = request.POST['f_stock']
            descripcion = request.POST['f_descripcion']
            InsumoComputacional.objects.create(numero_insumo=numero_insumo, nombre=nombre,
                                               fecha_adquisicion=fecha_adquisicion, marca=marca, stock=stock, descripcion=descripcion)
            mensaje = f"Se ha regitrado el Insumo computacional {numero_insumo} / {nombre} / {fecha_adquisicion}"
        except Exception as ex:
            if str(ex.__cause__).find('AppAdministracion_insumocomputacional.numero_insumo') > 0:
                mensaje = 'Ya existe un registro con ese numero de insumo'
        except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
        except:
            return render(request, "crudInsumosComputacion/agregarComputacion.html", {'mensaje': mensaje, "sesion_activa": sesion})
        return render(request, "crudInsumosComputacion/agregarComputacion.html", {'mensaje': mensaje, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def eliminarInsumo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    mensaje = None
    if sesion == 0 or sesion == 1:
        try:
            usr = InsumoComputacional.objects.get(
                numero_insumo=request.GET["numero_insumo"])
            usr.delete()
            mensaje = "Insumo eliminado"
            return render(request, 'crudInsumosComputacion/eliminarInsumo.html', {'mensaje': mensaje, "sesion_activa": sesion})
        except Exception as ex:
            if str(ex.args).find('does not exist') > 0:
                mensaje = 'Insumo no exite'
            else:
                mensaje = 'Ha ocurrido un problema'
            return render(request, "crudInsumosComputacion/eliminarInsumo.html", {mensaje: 'mensaje', "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def actualizarInsumo(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 1:
        usr = None
        msj = None
        try:
            usr = InsumoComputacional.objects.get(
                numero_insumo=request.GET["nInsumo"])
            return render(request, "crudInsumosComputacion/actualizarInsumo.html", {"usr": usr, "sesion_activa": sesion})
        except:
            usr = None

        if usr == None:
            numero_insumo = None
            try:
                numero_insumo = request.POST["f_numero_insumo"]
            except:
                numero_insumo = None

            if numero_insumo != None:
                usr = InsumoComputacional.objects.get(
                    numero_insumo=numero_insumo)
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
                return render(request, "crudInsumosComputacion/actualizarInsumo.html", {"msj": msj, "sesion_activa": sesion})
            else:
                msj = "No se ha encontrado el insumo"
                return render(request, "crudInsumosComputacion/actualizarInsumo.html", {"msj": msj, "sesion_activa": sesion})
        else:
            msj = "No se encontró el insumo solicitado"
            return render(request, "crudInsumosComputacion/actualizarInsumo.html", {"msj": msj, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def buscarInsumo(request):
    sesion = None
    datos = None
    visibilidad = "Hidden"
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 1:
        try:
            mensaje = ""
            for i in request.GET["buscarInsumo"]:
                if (i == chr(48) or i == chr(49) or i == chr(50) or
                    i == chr(51) or
                    i == chr(52) or i == chr(53) or i == chr(54) or
                        i == chr(55) or i == chr(56) or i == chr(57)):
                    mensaje = "Ingreso numero"
                else:
                    mensaje = "Ingreso letra"
                    break

            if mensaje == "Ingreso numero":
                datos = InsumoComputacional.objects.get(
                    numero_insumo=request.GET["buscarInsumo"])
                visibilidad = "visible"
                mensaje = "Insumo buscado por numero"

            elif mensaje == "Ingreso letra":
                datos = InsumoComputacional.objects.get(
                    nombre=request.GET["buscarInsumo"])
                visibilidad = "visible"
                mensaje = "Insumo buscado por nombre"

            return render(request, 'crudInsumosComputacion/buscarInsumo.html', {'mensaje': mensaje, "sesion_activa": sesion, "ins": datos, "visibilidad": visibilidad})
        except Exception as ex:
            mensaje = 'Error en la matrix'
        return render(request, "crudInsumosComputacion/buscarInsumo.html", {mensaje: 'mensaje', "sesion_activa": sesion, "visibilidad": visibilidad})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

# Funciones CRUD Oficina

def agregarOficina(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 3:
        try:
            mensaje = ""
            numero_articulo = request.POST['f_numero_oficina']
            nombre = request.POST['f_nombre_oficina']
            ubicacion = request.POST['f_ubicacion']
            stock = request.POST['f_stock_oficina']
            descripcion = request.POST['f_descripcion_oficina']
            ArticuloOficina.objects.create(
                numero_articulo=numero_articulo, nombre=nombre, ubicacion=ubicacion, stock=stock, descripcion=descripcion)
            mensaje = f"Se ha regitrado el Articulo de Oficina {numero_articulo} / {nombre} / {ubicacion}"
        except Exception as ex:
            if str(ex.__cause__).find('AppAdministracion_ArticuloOficina.numero_articulo') > 0:
                mensaje = 'Ya existe un registro con ese numero de este articulo'
        except Error as err:
            mensaje = f'ha ocurrido un problema en la operación_, {err}'
        except:
            return render(request, "agregarOficina/agregarOficina.html", {'mensaje': mensaje, "sesion_activa": sesion})
        return render(request, "agregarOficina/agregarOficina.html", {'mensaje': mensaje, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def listarOficina(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 3:
        oficina = ArticuloOficina.objects.all()
        return render(request, "agregarOficina/listarOficina.html", {"oficina": oficina, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def eliminarOficina(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 3:
        mensaje = None
        try:
            usr = ArticuloOficina.objects.get(
                numero_articulo=request.GET["numero_articulo"])
            usr.delete()
            mensaje = "Articulo de oficina eliminado"
            return render(request, 'agregarOficina/eliminarOficina.html', {'mensaje': mensaje, "sesion_activa": sesion})
        except Exception as ex:
            if str(ex.args).find('does not exist') > 0:
                mensaje = 'ARticulo de oficina no exite'
            else:
                mensaje = 'Ha ocurrido un problema'
            return render(request, "agregarOficina/eliminarOficina.html", {mensaje: 'mensaje', "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})

def actualizarOficina(request):
    sesion = None
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 3:
        usr = None
        msj = None
        try:
            usr = ArticuloOficina.objects.get(
                numero_articulo=request.GET["nOficina"])
            return render(request, "agregarOficina/actualizarOficina.html", {"usr": usr, "sesion_activa": sesion})
        except:
            usr = None

        if usr == None:
            numero_articulo = None
            try:
                numero_articulo = request.POST["f_numero_oficina"]
            except:
                numero_articulo = None

            if numero_articulo != None:
                usr = ArticuloOficina.objects.get(
                    numero_articulo=numero_articulo)
                nombre = request.POST['f_nombre_oficina']
                ubicacion = request.POST['f_ubicacion']
                stock = request.POST['f_stock_oficina']
                descripcion = request.POST['f_descripcion_oficina']

                usr.nombre = nombre
                usr.ubicacion = ubicacion
                usr.stock = stock
                usr.descripcion = descripcion
                try:
                    usr.save()
                    msj = "Se ha actualizado el articulo de oficina"
                except:
                    msj = f"ha ocurrido un error al actualizar el articulo"
                return render(request, "agregarOficina/actualizarOficina.html", {"msj": msj, "sesion_activa": sesion})
            else:
                msj = "No se ha encontrado el articulo"
                return render(request, "agregarOficina/actualizarOficina.html", {"msj": msj, "sesion_activa": sesion})
        else:
            msj = "No se encontró el insumo solicitado"
            return render(request, "agregarOficina/actualizarOficina.html", {"msj": msj, "sesion_activa": sesion})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})


def buscarOficina(request):
    sesion = None
    datos = None
    visibilidad = "Hidden"
    try:
        sesion = request.session['sesion_activa']
    except:
        return render(request, "iniciarSesion.html")
    if sesion == 0 or sesion == 3:
        try:
            mensaje = ""
            for i in request.GET["buscarOficina"]:
                if (i == chr(48) or i == chr(49) or i == chr(50) or
                    i == chr(51) or
                    i == chr(52) or i == chr(53) or i == chr(54) or
                        i == chr(55) or i == chr(56) or i == chr(57)):
                    mensaje = "Ingreso numero"
                else:
                    mensaje = "Ingreso letra"
                    break

            if mensaje == "Ingreso numero":
                datos = ArticuloOficina.objects.get(
                    numero_articulo=request.GET["buscarOficina"])
                visibilidad = "visible"
                mensaje = "Insumo buscado por numero"

            elif mensaje == "Ingreso nombre":
                datos = ArticuloOficina.objects.get(
                    nombre=request.GET["buscarOficina"])
                visibilidad = "visible"
                mensaje = "Insumo buscado por nombre"

            return render(request, 'agregarOficina/buscarOficina.html', {'mensaje': mensaje, "sesion_activa": sesion, "ins": datos, "visibilidad": visibilidad})
        except Exception as ex:
            mensaje = 'Error en la matrix'
        return render(request, "agregarOficina/buscarOficina.html", {mensaje: 'mensaje', "sesion_activa": sesion, "visibilidad": visibilidad})
    else:
        return render(request, "index.html", {'sesion_activa': sesion})
