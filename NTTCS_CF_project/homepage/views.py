import mimetypes
from time import sleep, time
from typing import Dict, Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView

import json

from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from acounts.models import User
from .models import Assessment, MaturirtyTable, AsociacionMarcos, Assessmentguardados, \
    NttcsCf20231, Domains, Evidencerequestcatalog, Evidencias, MapeoMarcos, AssessmentCreados, \
    AsociacionEvidenciasGenericas, AsociacionEvidenciasCreadas, TiposIniciativas, Iniciativas,\
    AssessmentEs, MaturirtyTableEs, EvidencerequestcatalogEs
from django.views.generic import TemplateView, ListView
import mysql.connector
from django.contrib import messages
import csv
import xlsxwriter
# IMPORT PARA DATATABLES
from django.http.response import JsonResponse
from django.template import loader


# Create your views here.

# Clase para la pagina del login
class index(LoginView):
    template_name = "homepage/index.html"

    def post(self, request):
        user = request.POST.get('user')
        pas = request.POST.get('pass')
        usuario = authenticate(request, username=user, password=pas)

        if usuario is not None:
            if usuario.last_login is None:
                login(request, usuario)
                return redirect('creacionPass')
            else:
                login(request, usuario)
                return redirect('menu')

        else:
            return render(request, self.template_name)


@login_required
def logout(request):
    logout(request)
    return redirect('/')


# funcion utilizada para comprobar que la contraseña intruducida es correcta
def contrasenaValida(password: str) -> bool:
    largo = False  # se pone a true si la cadena es lo suficientemente larga
    mayus = False  # se pone a true si la cadena contiene una mayuscula
    numerico = False  # se pone a true si la cadena contiene un numero
    caracterEspecial = False  # se pone a true si la cadena contiene un caracter especial /\.,:;!@#$%^&*()-_=+
    if len(password) > 8:  # comprobacion de longitud
        largo = True

    for i in password:
        if i.isupper():  # comprobacion de mayus
            mayus = True
        if i.isnumeric():  # comprobacion de numero
            numerico = True
        if i in '/\.,:;!@#$%^&*()-_=+':  # comprobacion de caracter especial
            caracterEspecial = True

    return largo and mayus and numerico and caracterEspecial  # retornemos and logico entre los 4 requerimientos


# Clase para la pagina de creacion de pass
class CreacionPass(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"

    template_name = "homepage/CreacionPass.html"

    def post(self, request, **knwargs):
        password = request.POST.get('password')  # valor del password
        passwordModificar = request.POST.get('passwordModificar')  # valor del passwordModificar
        password2Modificar = request.POST.get('password2Modificar')  # valor del password2Modificar
        user = request.user
        if password != '' and passwordModificar != '' and password2Modificar != '':  # comprobacion de entrega de cademas vacias
            if passwordModificar == password2Modificar:  # comprobacion de que las dos nuevas pass sean iguales
                if password != passwordModificar:  # coprobacion de que la contraseña nueva es distinta que la anterior
                    if user.check_password(password):  # comprobamos que la pass sea la correcta para el usuario
                        if contrasenaValida(
                                passwordModificar):  # comprobamos si la nueva pass cumple los requisitos de seguridad
                            user.set_password(passwordModificar)
                            user.save()
                            messages.success(request, 'La contraseña ha sido cambiada correctamente')
                            return redirect('logout')  # hacemos log out
                        else:
                            messages.error(request,
                                           'La contraseña debe contener, 8 caracteres, alguna mayuscula, algun caracter '
                                           'especial y algun numero')  # Se crea mensage de error
                    else:
                        messages.error(request, 'La contraseña no es correcta')  # Se crea mensage de error
                else:
                    messages.error(request,
                                   'La contraseña tiene que ser distinta a la anterior')  # Se crea mensage de error
            else:
                messages.error(request, 'Las contraseñas no coinciden')  # Se crea mensage de error
        else:
            messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error
        return render(request, self.template_name)


# Clase para la pagina de Perfil
class Perfil(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"

    template_name = "homepage/perfil.html"

    def post(self, request, **knwargs):
        password = request.POST.get('password')  # valor del password
        passwordModificar = request.POST.get('passwordModificar')  # valor del passwordModificar
        password2Modificar = request.POST.get('password2Modificar')  # valor del password2Modificar
        user = request.user
        if password != '' and passwordModificar != '' and password2Modificar != '':  # comprobacion de entrega de cademas vacias
            if passwordModificar == password2Modificar:  # comprobacion de que las dos nuevas pass sean iguales
                if password != passwordModificar:  # coprobacion de que la contraseña nueva es distinta que la anterior
                    if user.check_password(password):  # comprobamos que la pass sea la correcta para el usuario
                        if contrasenaValida(
                                passwordModificar):  # comprobamos si la nueva pass cumple los requisitos de seguridad
                            user.set_password(passwordModificar)
                            user.save()
                            messages.success(request,
                                             'La contraseña ha sido cambiada correctamente')  # Se crea mensage de error
                        else:
                            messages.error(request,
                                           'La contraseña debe contener, 8 caracteres, alguna mayuscula, algun caracter '
                                           'especial y algun numero')  # Se crea mensage de error
                    else:
                        messages.error(request, 'La contraseña no es correcta')  # Se crea mensage de error
                else:
                    messages.error(request,
                                   'La contraseña tiene que ser distinta a la anterior')  # Se crea mensage de error
            else:
                messages.error(request, 'Las contraseñas no coinciden')  # Se crea mensage de error
        else:
            messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error
        return render(request, self.template_name)


# Clase para la pagina de Usuarios
class Usuarios(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"

    template_name = "homepage/Usuarios.html"

    def get_context_data(self, **knwargs):
        context = super(Usuarios, self).get_context_data(**knwargs)
        context["grupos"] = Group.objects.all()  # contexto para el selector de gupos
        context["usuarios"] = User.objects.all()  # contexto para el selector de usuarios
        context["seleccionado"] = False  # variable para el despliegue de la modificacion de usuario
        return context

    def post(self, request, **knwargs):

        if 'boton3' in request.POST:  # if que recoge la pulsacion del boton de añadir usuario
            grupo = request.POST.get('selector')  # recogemos valor de selector de grupos
            nUsuario = request.POST.get('nUsuario')  # recogemos valor del nombre de usuario
            password = request.POST.get('password')  # recogemos el valor de la contraseña

            if grupo != 'None' and nUsuario != '' and password != '':  # comprobamos si todas las casillas esta rellenas.
                usuario = User.objects.create_user(username=nUsuario, password=password,
                                                   rol=grupo)  # creamos el usuario
                usuario.groups.add(Group.objects.get(name__in=[grupo]))  # le añadimos los permisos
                usuario.save()  # guardamos el usuario
            else:
                messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error

        elif 'selector1' in request.POST:  # if para la funcionalidad del selector
            if request.POST.get('selector1') == 'None':  # comprobamos si se selecciona el No Seleccionado
                context = super(Usuarios, self).get_context_data(**knwargs)
                context["grupos"] = Group.objects.all()
                context["usuarios"] = User.objects.all()
                context["seleccionado"] = False  # fijamos el desplegable a false
                return render(request, self.template_name, context=context)
            else:
                context = super(Usuarios, self).get_context_data(**knwargs)
                context["grupos"] = Group.objects.all()
                context["usuarios"] = User.objects.all()
                context["seleccionado"] = True  # fijamos el desplegable a true para que se muestre la info del usuario.
                usuarioSeleccionado = User.objects.get(username=request.POST.get('selector1'))  # fijamos el usuario
                context["seleccion"] = usuarioSeleccionado  # pasamos el usuario
                context["grupoSeleccionado"] = usuarioSeleccionado.groups.all()[0]  # pasamos el grupo del usuario
                # seleccionado
                request.session["usuarioSeleccionado"] = usuarioSeleccionado.username  # guardamos en la sesion el
                # usuario que se ha seleccioando.
                print(usuarioSeleccionado.password)
                return render(request, self.template_name, context=context)
        elif 'selector3' in request.POST:  # Recogemos el valor de los botones de modificar y eliminar.
            boton1 = request.POST.get('boton1')  # valor del boton 1
            grupo = request.POST.get('selector3')  # valor del boton 1
            nUsuarioModificar = request.POST.get('nUsuarioModificar')  # valor del nUsuarioModificar
            passwordModificar = request.POST.get('passwordModificar')  # valor del passwordModificar
            user = User.objects.get(username=request.session.get('usuarioSeleccionado'))  # recogemos el usuario
            # seleccionado en la sesion.
            if grupo != 'None' and nUsuarioModificar != '' and nUsuarioModificar != '':  # comprobamos que se hayan
                # rellenado todos los campos
                if boton1 == 'btn1':  # recogemos la pulsacion del boton modificar
                    user.username = nUsuarioModificar  # fijamos el nombre del usuario
                    user.groups.clear()  # limpiamos los permisos anteriores
                    user.groups.add(Group.objects.get(name__in=[grupo]))  # añadimos los nuevos permisos, pueden ser
                    # los mismos
                    if passwordModificar.startswith('pbkdf2_sha256$'):  # comprobamos si el valor de la contraseña es
                        # la hasheada, osea la anterior, no podemos saber el valor sin hashear
                        user.password = passwordModificar
                    else:  # si no es el valor hasheado lo tenemos que encriptar
                        user.set_password(passwordModificar)  # para eso usamos el set_password
                    user.save()
                else:  # recogemos la pulsacion del boton Eliminar
                    user.delete()  # eliminamos el usuario seleccioando
            else:
                messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error

        context = super(Usuarios, self).get_context_data(**knwargs)
        context["grupos"] = Group.objects.all()
        context["usuarios"] = User.objects.all()
        return render(request, self.template_name, context=context)


# Clase para la pagina de Assessment
class assessment(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"

    template_name = "homepage/assessment.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    def contextTotal(self, request, select, assSelect, context):

        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
        context["NombreAss"] = assSelect
        context["assessment"] = assGuardado
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        if assGuardado.idioma == 'en':
            context["valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
        else:
            context["valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
        request.session["controlSelect"] = select
        control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=select)
        context["control"] = control
        context["criteriovaloracion"] = control.criteriovaloracion.split('\n')
        context["evidencias"] = AsociacionEvidenciasGenericas.objects.filter(assessment=control)
        context["evidencias2"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment=control)
        context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
        context["tiposIniciativas"] = TiposIniciativas.objects.all()
        context["iniciativas"] = Iniciativas.objects.all()
        evidenciasRecomendadas = Assessment.objects.get(id=select).evidence_request_references
        if evidenciasRecomendadas == '' or evidenciasRecomendadas is None:
            context["recomendacion"] = False
        else:

            evidenciasRecomendadas = evidenciasRecomendadas.split('\n')
            r = ''
            for i in evidenciasRecomendadas:
                if assGuardado.idioma == 'en':
                    evidencia = Evidencerequestcatalog.objects.get(evidence_request_references=i)
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia=evidencia, assessment=control):
                        r += i + ', '
                else:
                    evidencia = EvidencerequestcatalogEs.objects.get(evidence_request_references=i)
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia_id_es=evidencia, assessment=control):
                        r += i + ', '
            if r != '':
                context["recomendacion"] = True
                context["eviRecomendada"] = r[:len(r)-2]
            else:
                context["recomendacion"] = False
        return request, context

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        assSelect = self.request.session.get('assessmentGuardado')
        context = super(assessment, self).get_context_data(**knwargs)
        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        if assGuardado.idioma == 'en':
            context["valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
        else:
            context[
                "valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
        context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
        context["tiposIniciativas"] = TiposIniciativas.objects.all()
        context["iniciativas"] = Iniciativas.objects.all()
        self.request.session["controlSelect"] = 'noSel'
        return context

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):
        assSelect = request.session.get('assessmentGuardado')
        select = request.POST.get('selector')  # valor de el selector de control
        boton = request.POST.get('boton')  # valor del boton 1
        boton2 = request.POST.get('boton2')  # valor del boton 2
        boton3 = request.POST.get('boton3')  # valor del boton 3
        boton4 = request.POST.get('boton4')  # valor del boton 4
        boton5 = request.POST.get('boton5')  # valor del boton 5
        boton6 = request.POST.get('boton6')  # valor del boton 6
        boton7 = request.POST.get('boton7')  # valor del boton 7
        boton8 = request.POST.get('boton8')  # valor del boton 7

        if 'selector' in request.POST:  # se recoge la pulsacion del select
            if select == 'noSel':
                context = super(assessment, self).get_context_data(**knwargs)
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
                if assGuardado.idioma == 'en':
                    context[
                        "valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
                else:
                    context[
                        "valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
                request.session["controlSelect"] = select
                context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                context["iniciativas"] = Iniciativas.objects.all()
                return render(request, self.template_name, context=context)
            else:
                context = super(assessment, self).get_context_data(**knwargs)
                request, context = self.contextTotal(request, select, assSelect, context)
                return render(request, self.template_name, context=context)

        elif boton2 == 'btn2':  # recogemos la pulsacion del boton de guardar valoracion
            if request.session["controlSelect"] != 'noSel':
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=request.session["controlSelect"])
                control.respuesta = str(request.POST.get('respuesta'))
                control.valoracion = request.POST.get('valmad')
                control.valoracionobjetivo = request.POST.get('valmadob')
                control.save()

            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
            context = super(assessment, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session.get('controlSelect'), assSelect, context)
            return render(request, self.template_name, context=context)
        elif boton4 == 'btn4':  # if encargado de rellenar las evidencias

            idEvidencia = request.POST.get('idEvidencia') + '-C'  # valor del idEvidencia
            descripcionEvidencia = request.POST.get('DescripcionEvidencia')  # valor del DescripcionEvidencia
            linkEvidencia = request.POST.get('linkEvidencia')  # valor del linkEvidencia
            controlId = request.session["controlSelect"]

            if controlId != 'noSel':
                if idEvidencia != '' and descripcionEvidencia != '':  # recogemos la pulsacion de guardar la evidencia
                    if not Evidencias.objects.filter(evidencia_id=idEvidencia).exists():

                        ev = Evidencias(evidencia_id=idEvidencia, comentario=descripcionEvidencia, links=linkEvidencia,
                                        control_id=controlId,
                                        assessment=Assessmentguardados.objects.get(id_assessment=assSelect))
                        ev.save()
                        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                        control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                control_id=request.session["controlSelect"])
                        control.respuesta = str(request.POST.get('respuesta'))
                        control.valoracion = request.POST.get('valmad')
                        control.valoracionobjetivo = request.POST.get('valmadob')

                        evidencia = AsociacionEvidenciasCreadas(id_evidencia=ev, id_assessment=control)
                        evidencia.save()
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, assSelect, context)
                        return render(request, self.template_name, context=context)
                    else:
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, assSelect, context)
                        messages.error(request,
                                       'EVIDENCIA INCORRECTA: La evidencia introducida ya existe')  # Se crea mensage de error
                        return render(request, self.template_name, context=context)
                else:
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, controlId, assSelect, context)
                    messages.error(request, 'EVIDENCIA INCORRECTA Necesita introducir un id y una descripcion para la '
                                            'evidencia')  # Se crea mensage de error
                    return render(request, self.template_name, context=context)
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(assessment, self).get_context_data(**knwargs)
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
                if assGuardado.idioma == 'en':
                    context[
                        "valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
                else:
                    context[
                        "valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
                context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                context["iniciativas"] = Iniciativas.objects.all()
                return render(request, self.template_name, context=context)

        elif boton5 == 'btn5':  # if encargado de rellenar las evidencias
            if request.session["controlSelect"] != 'noSel':
                selectorEvidencia = request.POST.get('selectorEvidencia')  # valor de el selector de control
                if selectorEvidencia != 'noSel':
                    assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                    control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                            control_id=request.session["controlSelect"])
                    if assGuardado.idioma == 'en':
                        evidencia = Evidencerequestcatalog.objects.get(evidence_request_references=selectorEvidencia)
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia=evidencia,assessment=control)
                        eviGenerica.save()
                    else:
                        evidencia = EvidencerequestcatalogEs.objects.get(evidence_request_references=selectorEvidencia)
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia_id_es=evidencia, assessment=control)
                        eviGenerica.save()
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)
                    return render(request, self.template_name, context=context)
                else:
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)
                    messages.error(request, 'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')  # Se crea mensage de error
                    return render(request, self.template_name, context=context)
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(assessment, self).get_context_data(**knwargs)
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
                if assGuardado.idioma == 'en':
                    context[
                        "valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
                else:
                    context[
                        "valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
                context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                context["iniciativas"] = Iniciativas.objects.all()
                return render(request, self.template_name, context=context)
        elif boton6 == 'btn6':  # if encargado de rellenar las evidencias
            selectorEvidencia = request.POST.get('selectorEvidenciaIniciativa')
            nombreIniciativa = request.POST.get('nombreIniciativa')
            DescripcionIniciativa = request.POST.get('DescripcionIniciativa')
            SelectorIniciativa = request.POST.get('SelectorIniciativa')
            if request.session["controlSelect"] != 'noSel':
                if selectorEvidencia != 'noSel':
                    if not Iniciativas.objects.filter(nombre=nombreIniciativa).exists():
                        if Evidencerequestcatalog.objects.filter(evidence_request_references=selectorEvidencia).exists():

                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])
                            if assGuardado.idioma == 'en':
                                evidencia = Evidencerequestcatalog.objects.get(
                                    evidence_request_references=selectorEvidencia)
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia=evidencia, assessment=control)
                            else:
                                evidencia = EvidencerequestcatalogEs.objects.get(
                                    evidence_request_references=selectorEvidencia)

                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia_id_es=evidencia, assessment=control)

                            tipoIniciativa = TiposIniciativas.objects.get(tipo=SelectorIniciativa)
                            iniciativa = Iniciativas(nombre=nombreIniciativa, descripcion=DescripcionIniciativa, tipo=tipoIniciativa)
                            iniciativa.save()

                            asociacion.iniciativa = iniciativa
                            asociacion.save()
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)
                            return render(request, self.template_name, context=context)
                        else:
                            evidencia = Evidencias.objects.get(evidencia_id=selectorEvidencia)
                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])
                            asociacion = AsociacionEvidenciasCreadas.objects.get(id_evidencia=evidencia, id_assessment=control)

                            tipoIniciativa = TiposIniciativas.objects.get(tipo=SelectorIniciativa)
                            iniciativa = Iniciativas(nombre=nombreIniciativa, descripcion=DescripcionIniciativa,
                                                     tipo=tipoIniciativa)
                            iniciativa.save()

                            asociacion.iniciativa = iniciativa
                            asociacion.save()
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)
                            return render(request, self.template_name, context=context)
                    else:
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                             context)
                        messages.error(request,
                                       'INICIATIVA INCORRECTA: El nombre introducido ya esta en uso')  # Se crea mensage de error
                        return render(request, self.template_name, context=context)
                else:
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)
                    messages.error(request,
                                   'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')  # Se crea mensage de error
                    return render(request, self.template_name, context=context)
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(assessment, self).get_context_data(**knwargs)
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
                if assGuardado.idioma == 'en':
                    context[
                        "valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
                else:
                    context[
                        "valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
                context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                context["iniciativas"] = Iniciativas.objects.all()
                return render(request, self.template_name, context=context)
        elif boton7 == 'btn7':  # if encargado de rellenar las evidencias
            selectEviasig = request.POST.get('selectEviasig')
            selectIniAsig = request.POST.get('selectIniAsig')
            if request.session["controlSelect"] != 'noSel':
                if selectEviasig != 'noSel':
                    if selectIniAsig != 'noSel':
                        if Evidencerequestcatalog.objects.filter(
                                evidence_request_references=selectEviasig).exists():


                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])

                            if assGuardado.idioma == 'en':
                                evidencia = Evidencerequestcatalog.objects.get(
                                    evidence_request_references=selectEviasig)
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia=evidencia,
                                                                                       assessment=control)
                            else:
                                evidencia = Evidencerequestcatalog.objects.get(
                                    evidence_request_references=selectEviasig)
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia_id_es=evidencia,
                                                                                       assessment=control)


                            iniciativa = Iniciativas.objects.get(nombre=selectIniAsig)
                            asociacion.iniciativa = iniciativa
                            asociacion.save()
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)
                            return render(request, self.template_name, context=context)
                        else:
                            evidencia = Evidencias.objects.get(evidencia_id=selectEviasig)
                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])
                            asociacion = AsociacionEvidenciasCreadas.objects.get(id_evidencia=evidencia,
                                                                                 id_assessment=control)

                            iniciativa = Iniciativas.objects.get(nombre=selectIniAsig)
                            asociacion.iniciativa = iniciativa
                            asociacion.save()
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)
                            return render(request, self.template_name, context=context)
                    else:
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                             context)
                        messages.error(request,
                                       'INICIATIVA INCORRECTA: Necesita seleccionar una iniciativa')  # Se crea mensage de error
                        return render(request, self.template_name, context=context)
                else:
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                         context)
                    messages.error(request,
                                   'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')  # Se crea mensage de error
                    return render(request, self.template_name, context=context)
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(assessment, self).get_context_data(**knwargs)
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

                if assGuardado.idioma == 'en':
                    context[
                        "valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez
                    context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                else:
                    context[
                        "valMad"] = MaturirtyTableEs.objects.all()  # consulta para el desplegable de la valoracion de madurez
                    context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                context["iniciativas"] = Iniciativas.objects.all()
                return render(request, self.template_name, context=context)
        elif boton8 == 'btn8':  # if encargado de rellenar las evidencias
            evidenciasRecomendadas = Assessment.objects.get(id=request.session["controlSelect"]).evidence_request_references.split('\n')
            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

            for i in evidenciasRecomendadas:
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                if assGuardado.idioma == 'en':
                    evidencia = Evidencerequestcatalog.objects.get(
                        evidence_request_references=i)
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia=evidencia, assessment=control):
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia=evidencia, assessment=control)
                        eviGenerica.save()
                else:
                    evidencia = EvidencerequestcatalogEs.objects.get(
                        evidence_request_references=i)
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia_id_es=evidencia, assessment=control):
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia_id_es=evidencia, assessment=control)
                        eviGenerica.save()

            context = super(assessment, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)
            return render(request, self.template_name, context=context)
        else:  # se recoge la pulsacion del boton de archivar tras la confirmacion

            consulta = Assessmentguardados.objects.get(
                id_assessment=assSelect)  # colsulta para la selecionar el assesment
            consulta.archivado = 1  # ponemos el valor de archivado a 1
            consulta.save()
            return redirect('menu')  # volvemos al menu




# Clase para la pagina de AssessmentSelect

class assessmentselect(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/assessmentselect.html"

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(assessmentselect, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.filter(archivado=0)
        context["marcos"] = AsociacionMarcos.objects.all()
        return context

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):
        nombre = request.POST.get('in')  # Valor del input de nombre
        select = request.POST.get('selector1')  # valor de selector de assesment guardado
        select2 = request.POST.getlist('selector2')  # valor de selector de marcos para la creacion del assesment
        idioma = request.POST.getlist('idioma')  # valor de selector de marcos para la creacion del assesment

        if 'selector1' in request.POST:
            request.session["assessmentGuardado"] = select
            return redirect("assessment")

        elif nombre != '' and select2 != None:
            if Assessmentguardados.objects.filter(id_assessment=nombre).exists() == False:
                assessmentNuevo = Assessmentguardados(id_assessment=nombre,
                                        archivado=0, idioma=idioma)  # creamos una nueva fila en assessmentguardados con el string de marcos y el nombre del marco
                assessmentNuevo.save()

                marcos = ''
                marc = []
                for i in select2:  # recorremos el segundo selector
                    consulta = AsociacionMarcos.objects.get(marco_id=i).nombre_tabla
                    c = MapeoMarcos.objects.extra(
                        where=[consulta + "='1'"])  # query para seleccionar la tabla del marco seleccionado
                    for fila in c:
                        if fila.ntt_id not in marc:
                            marc += [fila.ntt_id]  # recorremos la tabla del marco cogiendo los controles de ntt
                            # que no este repetidos

                for marco in marc:
                    marcos += marco + '\n'  # creamos un string con todos los controles de ntt separados por intros
                    if idioma == 'en':
                        consulta = Assessment.objects.get(id=marco)
                    else:
                        consulta = AssessmentEs.objects.get(id=marco)
                    criterioVal = consulta.campo9 + '\n' + consulta.campo10 + '\n' + consulta.campo11 + '\n' + consulta.campo12 + '\n' + consulta.campo13 + '\n' + consulta.campo14

                    a = AssessmentCreados(assessment=assessmentNuevo, control_id=str(marco), control_name=consulta.control,
                                          descripcion=consulta.control_description, pregunta=consulta.control_question,
                                          criteriovaloracion=criterioVal)
                    a.save()

                assessmentNuevo.marcos = marcos
                assessmentNuevo.save()

                request.session["assessmentGuardado"] = nombre
                return redirect("assessment")
            else:
                messages.error(request, 'El Assessment ya exsiste.')
                context = super().get_context_data(**knwargs)
                context["assess"] = Assessmentguardados.objects.filter(archivado=0)
                context["marcos"] = AsociacionMarcos.objects.all()
                return render(request, self.template_name, context=context)
        elif nombre == '' and select2 is not None:  # if donde se recoge si se ha introducido valores de marcos paro no de nombre para el assessment

            messages.error(request, 'Necesitas introducir un nombre para el Assessment')  # Se crea mensage de error
            context = super().get_context_data(**knwargs)
            context["assess"] = Assessmentguardados.objects.filter(archivado=0)
            context["marcos"] = AsociacionMarcos.objects.all()
            return render(request, self.template_name, context=context)
        else:  # este else esta por si se toca algun boton pero no hay ninguna cosa seleccionada.
            context = super().get_context_data(**knwargs)
            context["assess"] = Assessmentguardados.objects.filter(archivado=0)
            context["marcos"] = AsociacionMarcos.objects.all()
            return render(request, self.template_name, context=context)


# Clase para la pagina de Exportaciones
class Exportaciones(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/Exportaciones.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')  # constante para la conexion con la base de datos

    def get_context_data(self, **knwargs):
        context = super(Exportaciones, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.all()
        return context

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):
        selector = request.POST.get('selector1')
        excel = request.POST.get('excel')
        csvinput = request.POST.get('csv')
        word = request.POST.get('word')
        if selector != 'None':
            ass = Assessmentguardados.objects.get(id_assessment=selector)
            consulta = AssessmentCreados.objects.filter(assessment=ass)
            valores = []

            for fila in consulta:  # Rellenamos tanto las casillas de respuesta y valoracion
                evgen = AsociacionEvidenciasGenericas.objects.filter(assessment=fila)
                evcre = AsociacionEvidenciasCreadas.objects.filter(id_assessment=fila)
                evidencias = ''
                for i in evgen:
                    evidencias += i.evidencia.evidence_request_references+'\n'
                for i in evcre:
                    evidencias += i.id_evidencia.evidencia_id+'\n'

                valores += {
                    'idControl': fila.control_id,
                    'nControl': fila.control_name,
                    'descripcion': fila.descripcion,
                    'pregunta': fila.pregunta,
                    'respuesta': fila.respuesta,
                    'valoracion': fila.valoracion,
                    'valoracionObjetivo': fila.valoracionobjetivo,
                    'criterio': fila.criteriovaloracion,
                    'evidencias': evidencias
                },

            titulos = ["idControl", "nControl", "descripcion", "pregunta", "respuesta", "valoracion", "valoracionObjetivo", "criterio",
                       "evidencias"]
            now = datetime.now()
            filename = 'Exportaciones/' + selector + '_Export_' + str(now.day) + '_' + str(now.month) + '_' + str(
                now.year) + '_' + str(now.hour) + '_' + str(now.minute)
            if 'csv' == csvinput:
                filename += '.csv'
                with open(filename, mode='w', encoding="cp437", errors="replace") as file:
                    writer = csv.DictWriter(file, delimiter=',', fieldnames=titulos)
                    writer.writeheader()

                    for valor in valores:
                        writer.writerow(valor)

                path = open(filename, 'r')
                mime_type, _ = mimetypes.guess_type(filename)
                response = HttpResponse(path, content_type=mime_type)
                response['Content-Disposition'] = f"attachment; filename={filename}"
                return response

            if 'excel' == excel:
                filename += '.xlsx'
                workbook = xlsxwriter.Workbook(filename)
                workbook.encoding = "utf-8"
                worksheet = workbook.add_worksheet()

                for row, _dict in enumerate(valores):
                    for col, key in enumerate(titulos):
                        worksheet.write(row, col, _dict[key])
                workbook.close()

                with open(filename, "rb") as file:
                    response = HttpResponse(file.read(),
                                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    response['Content-Disposition'] = f"attachment; filename={filename}"
                return response

            if 'word' == word:
                pass
        context = super(Exportaciones, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.all()
        return render(request, self.template_name, context=context)


# Clase para la pagina de informes
class informes(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/informes.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')  # constante para la conexion con la base de datos

    def get_context_data(self, **knwargs):
        context = super(informes, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.all()
        return context


# Clase para la pagina de Mantenimiento
class Mantenimiento(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/Mantenimiento.html"


# Clase para la pagina de MantenimientoNivelMadurez
class MantenimientoNivelMadurez(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoNivelMadurez.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:
            Ccmmcod = request.POST.get('Ccmmcod')  # valor del input de ccmmcod
            Description = request.POST.get('Description')  # valor del input de descripcion
            Sublevels = request.POST.get('Sublevels')  # valor del input de sublevels
            if request.POST.get('Percentage') == '':
                Percentage = request.POST.get('Percentage')  # valor del input de percentaje
            else:
                Percentage = float(request.POST.get('Percentage').replace(',', '.'))  # valor del input de percentaje
            if not MaturirtyTable.objects.filter(sublevels=Sublevels).exists():
                if Ccmmcod != '' and Description != '' and Sublevels != '' and Percentage != '':
                    insert = MaturirtyTable(ccmmcod=Ccmmcod, description=Description, sublevels=Sublevels,
                                            percentage=Percentage)  # creamos un nuevo input en la tabla
                    insert.save()
                else:
                    messages.error(request,
                                   'ERROR, debe introducir todos los valores para insertar un nivel de madurez')
            else:
                messages.error(request, 'ERROR, el sublevel debe ser distinto a uno ya existente')
        elif 'modificar' in request.POST:
            Ccmmcod = request.POST.get('Ccmmcod')  # valor del input de ccmmcod
            Description = request.POST.get('Description')  # valor del input de descripcion
            Sublevels = request.POST.get('Sublevels')  # valor del input de sublevels
            Percentage = float(request.POST.get('Percentage').replace(',', '.'))  # valor del input de percentaje
            consulta = MaturirtyTable.objects.get(
                sublevels=Sublevels)  # si esta en la tabla seleccionamos el ojeto en la tabla
            consulta.ccmmcod = Ccmmcod
            consulta.description = Description
            consulta.percentage = Percentage
            consulta.save()  # fijamos los valores y los guardamos.
        elif 'eliminar' in request.POST:
            Sublevels = request.POST.get('Sublevels')  # valor del input de sublevels
            consulta = MaturirtyTable.objects.get(sublevels=Sublevels)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(MaturirtyTable.objects.all(), 50)
        context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(MaturirtyTable.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(MaturirtyTable.objects.all(), 50)
        context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(MaturirtyTable.objects.all())
        return context


# Clase para la pagina de inicio de sesion


# Clase para la pagina de menu
class menu(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/menu.html"


# Clase para la pagina de MantenimientoDominios
class MantenimientoDominios(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoDominios.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:
            identifier = request.POST.get('identifier')  # valor del input de identifier
            domain = request.POST.get('domain')  # valor del input de domain
            security_privacy_by_design_s_p_principles = request.POST.get(
                'security_privacy_by_design_s_p_principles')  # valor del input de security_privacy_by_design_s_p_principles
            principle_intent = request.POST.get('principle_intent')  # valor del input de principle_intent
            if not Domains.objects.filter(identifier=identifier).exists():
                if identifier != '' and domain != '' and security_privacy_by_design_s_p_principles != '' and principle_intent != '':
                    insert = Domains(identifier=identifier, domain=domain,
                                     security_privacy_by_design_s_p_principles=security_privacy_by_design_s_p_principles,
                                     principle_intent=principle_intent, )  # creamos un nuevo input en la tabla
                    insert.save()
                else:
                    messages.error(request, 'ERROR, debe introducir todos los valores para insertar un dominio')
            else:
                messages.error(request, 'ERROR, el identifier debe ser distinto a uno ya existente')
        elif 'modificar' in request.POST:
            identifier = request.POST.get('identifier')  # valor del input de identifier
            domain = request.POST.get('domain')  # valor del input de domain
            security_privacy_by_design_s_p_principles = request.POST.get(
                'security_privacy_by_design_s_p_principles')  # valor del input de security_privacy_by_design_s_p_principles
            principle_intent = request.POST.get('principle_intent')  # valor del input de principle_intent
            consulta = Domains.objects.get(
                identifier=identifier)  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
            consulta.domain = domain
            consulta.security_privacy_by_design_s_p_principles = security_privacy_by_design_s_p_principles
            consulta.principle_intent = principle_intent
            consulta.save()  # fijamos los valores y los guardamos.
        elif 'eliminar' in request.POST:
            identifier = request.POST.get('identifier')  # valor del input de identifier

            consulta = Domains.objects.get(identifier=identifier)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(Domains.objects.all(), 50)
        context = super(MantenimientoDominios, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(Domains.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(Domains.objects.all(), 50)
        context = super(MantenimientoDominios, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(Domains.objects.all())
        return context

    # Funcion utilizada para eliminar el valor seleccionado de la tabla


# Clase para la pagina de MantenimientoEvidencias
class MantenimientoEvidencias(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoEvidencias.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:

            evidence_request_references = request.POST.get(
                'evidence_request_references')  # valor del input de evidence_request_references
            area_of_focus = request.POST.get('area_of_focus')  # valor del input de area_of_focus
            artifact = request.POST.get('artifact')  # valor del input de artifact
            artifact_description = request.POST.get('artifact_description')  # valor del input de artifact_description
            control_mappings = request.POST.get('control_mappings')  # valor del input de control_mappings
            if not Evidencerequestcatalog.objects.filter(
                    evidence_request_references=evidence_request_references).exists():
                if evidence_request_references != '' and area_of_focus != '' and artifact != '' and artifact_description != '' and control_mappings != '':
                    insert = Evidencerequestcatalog(evidence_request_references=evidence_request_references,
                                                    area_of_focus=area_of_focus, artifact=artifact,
                                                    artifact_description=artifact_description,
                                                    control_mappings=control_mappings)  # creamos un nuevo input en la tabla
                    insert.save()
                else:
                    messages.error(request, 'ERROR, debe introducir todos los valores para insertar una Evidencia')
            else:
                messages.error(request, 'ERROR, la evidence_request_references debe ser distinto a uno ya existente')
        elif 'modificar' in request.POST:
            evidence_request_references = request.POST.get(
                'evidence_request_references')  # valor del input de evidence_request_references
            area_of_focus = request.POST.get('area_of_focus')  # valor del input de area_of_focus
            artifact = request.POST.get('artifact')  # valor del input de artifact
            artifact_description = request.POST.get('artifact_description')  # valor del input de artifact_description
            control_mappings = request.POST.get('control_mappings')  # valor del input de control_mappings
            consulta = Evidencerequestcatalog.objects.get(
                evidence_request_references=evidence_request_references)  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
            consulta.area_of_focus = area_of_focus
            consulta.artifact = artifact
            consulta.artifact_description = artifact_description
            consulta.control_mappings = control_mappings
            consulta.save()  # fijamos los valores y los guardamos.
        elif 'eliminar' in request.POST:
            evidence_request_references = request.POST.get(
                'evidence_request_references')  # valor del input de evidence_request_references

            consulta = Evidencerequestcatalog.objects.get(evidence_request_references=evidence_request_references)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(Evidencerequestcatalog.objects.all(), 50)
        context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(Evidencerequestcatalog.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(Evidencerequestcatalog.objects.all(), 50)
        context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(Evidencerequestcatalog.objects.all())
        return context

    # Funcion utilizada para eliminar el valor seleccionado de la tabla


# Clase para la pagina de MantenimientoPreguntas
class MantenimientoPreguntas(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoPreguntas.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:
            control_question = request.POST.get('control_question')  # valor del input de control_question
            control_description = request.POST.get('control_description')  # valor del input de control_description
            id = request.POST.get('id')  # valor del input de id
            if not Assessment.objects.filter(id=id).exists():
                if control_question != '' and control_description != '' and id != '':
                    insert = Assessment(id=id, control_question=control_question,
                                        control_description=control_description)  # creamos un nuevo input en la tabla
                    insert.save()
                else:
                    messages.error(request, 'ERROR, debe introducir todos los valores para insertar una Pregunta')
            else:
                messages.error(request, 'ERROR, el id debe ser distinto a uno ya existente')
        elif 'modificar' in request.POST:
            control_question = request.POST.get('control_question')  # valor del input de control_question
            control_description = request.POST.get('control_description')  # valor del input de control_description
            id = request.POST.get('id')  # valor del input de id
            consulta = Assessment.objects.get(id=id)  # si esta en la tabla seleccionamos el ojeto en la tabla
            consulta.control_description = control_description
            consulta.control_question = control_question
            consulta.save()  # fijamos los valores y los guardamos..
        elif 'eliminar' in request.POST:
            id = request.POST.get('id')  # valor del input de id

            consulta = Assessment.objects.get(id=id)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(Assessment.objects.all(), 50)
        context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(Assessment.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(Assessment.objects.all(), 50)
        context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(Assessment.objects.all())
        return context


# Clase para la pagina de MantenimientoMarcosExistentes
class MantenimientoMarcosExistentes(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoMarcosExistentes.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):
        if 'insertar' in request.POST:
            marco_id = request.POST.get('marco_id')  # valor del input de marco_id
            nombre_tabla = request.POST.get('nombre_tabla')  # valor del input de nombre_tabla
            if not AsociacionMarcos.objects.filter(marco_id=marco_id).exists():
                if marco_id != '' and nombre_tabla != '':
                    insert = AsociacionMarcos(marco_id=marco_id,
                                              nombre_tabla=nombre_tabla)  # creamos un nuevo input en la tabla
                    insert.save()
                else:
                    messages.error(request, 'ERROR, debe introducir todos los valores para insertar un marco')
            else:
                messages.error(request, 'ERROR, el marco_id debe ser distinto a uno ya existente')
        elif 'modificar' in request.POST:
            marco_id = request.POST.get('marco_id')  # valor del input de marco_id
            nombre_tabla = request.POST.get('nombre_tabla')  # valor del input de nombre_tabla

            consulta = AsociacionMarcos.objects.get(
                marco_id=marco_id)  # si esta en la tabla seleccionamos el ojeto en la tabla
            consulta.nombre_tabla = nombre_tabla
            consulta.save()  # fijamos los valores y los guardamos.
        elif 'eliminar' in request.POST:
            marco_id = request.POST.get('marco_id')  # valor del input de marco_id
            consulta = AsociacionMarcos.objects.get(marco_id=marco_id)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(AsociacionMarcos.objects.all(), 50)
        context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(AsociacionMarcos.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(AsociacionMarcos.objects.all(), 50)
        context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(AsociacionMarcos.objects.all())
        return context

    # Funcion utilizada para eliminar el valor seleccionado de la tabla

class listadoControles(LoginRequiredMixin, ListView):

    model = NttcsCf20231

    def get_queryset(self):
        return self.model.objects.all().values()

    def get(self, request, *args, **kwargs):
        inicio = int(request.GET.get('inicio'))
        fin = int(request.GET.get('limite'))
        tiempo_inicial = time()
        data = self.get_queryset()
        list_data = []
        for indice, valor in enumerate(data[inicio: inicio+fin]):
            list_data.append(valor)
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución: {tiempo_final}')

        data = {
            'length': data.count(),
            'object': list_data
        }

        return HttpResponse(json.dumps(data), 'application/json')


# Clase para la pagina de MantenimientoControlesNTTCS
class MantenimientoControlesNTTCS(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoControlesNTTCS.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:
            domain = request.POST.get('domain')  # valor del input de domain
            selected_y_n_field = request.POST.get('selected_y_n_field')  # valor del input de selected_y_n_field
            control = request.POST.get('control')  # valor del input de control
            id = request.POST.get('id')  # valor del input de id
            control_description = request.POST.get('control_description')  # valor del input de control_description
            relative_control_weighting = request.POST.get(
                'relative_control_weighting')  # valor del input de relative_control_weighting
            function_grouping = request.POST.get('function_grouping')  # valor del input de function_grouping
            assesed_result = request.POST.get('assesed_result')  # valor del input de assesed_result
            numeric_result = request.POST.get('numeric_result')  # valor del input de numeric_result
            weighted_numeric_result = request.POST.get(
                'weighted_numeric_result')  # valor del input de weighted_numeric_result
            assessment_comments = request.POST.get('assessment_comments')  # valor del input de assessment_comments
            relative_result_by_function = request.POST.get(
                'relative_result_by_function')  # valor del input de relative_result_by_function
            relative_result_by_domain = request.POST.get(
                'relative_result_by_domain')  # valor del input de relative_result_by_domain
            if not NttcsCf20231.objects.filter(id=id).exists():
                if domain != '' and selected_y_n_field != '' and control != '' and id != '' and control_description != '' and relative_control_weighting != '' and function_grouping != '' and assesed_result != '' and numeric_result != '' and weighted_numeric_result != '' and assessment_comments != '' and relative_result_by_function != '' and relative_result_by_domain != '':
                    insert = NttcsCf20231(domain=domain, selected_y_n_field=selected_y_n_field, id=id, control=control,
                                          control_description=control_description,
                                          relative_control_weighting=relative_control_weighting,
                                          function_grouping=function_grouping, assesed_result=assesed_result,
                                          numeric_result=numeric_result,
                                          weighted_numeric_result=weighted_numeric_result,
                                          assessment_comments=assessment_comments,
                                          relative_result_by_function=relative_result_by_function,
                                          relative_result_by_domain=relative_result_by_domain)  # creamos un nuevo input en la tabla
                    insert.save()
                else:
                    messages.error(request, 'ERROR, debe introducir todos los valores para insertar un control')
            else:
                messages.error(request, 'ERROR, el id debe ser distinto a uno ya existente')
        elif 'modificar' in request.POST:
            domain = request.POST.get('domain')  # valor del input de domain
            selected_y_n_field = request.POST.get('selected_y_n_field')  # valor del input de selected_y_n_field
            control = request.POST.get('control')  # valor del input de control
            id = request.POST.get('id')  # valor del input de id
            control_description = request.POST.get('control_description')  # valor del input de control_description
            relative_control_weighting = request.POST.get(
                'relative_control_weighting')  # valor del input de relative_control_weighting
            function_grouping = request.POST.get('function_grouping')  # valor del input de function_grouping
            assesed_result = request.POST.get('assesed_result')  # valor del input de assesed_result
            numeric_result = request.POST.get('numeric_result')  # valor del input de numeric_result
            weighted_numeric_result = request.POST.get(
                'weighted_numeric_result')  # valor del input de weighted_numeric_result
            assessment_comments = request.POST.get('assessment_comments')  # valor del input de assessment_comments
            relative_result_by_function = request.POST.get(
                'relative_result_by_function')  # valor del input de relative_result_by_function
            relative_result_by_domain = request.POST.get(
                'relative_result_by_domain')  # valor del input de relative_result_by_domain
            consulta = NttcsCf20231.objects.get(id=id)  # si esta en la tabla seleccionamos el ojeto en la tabla
            consulta.domain = domain
            consulta.selected_y_n_field = selected_y_n_field
            consulta.control = control
            consulta.control_description = control_description
            consulta.relative_control_weighting = relative_control_weighting
            consulta.function_grouping = function_grouping
            consulta.assesed_result = assesed_result
            consulta.numeric_result = numeric_result
            consulta.weighted_numeric_result = weighted_numeric_result
            consulta.assessment_comments = assessment_comments
            consulta.relative_result_by_function = relative_result_by_function
            consulta.relative_result_by_domain = relative_result_by_domain
            consulta.save()  # fijamos los valores y los guardamos.
        elif 'eliminar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            consulta = NttcsCf20231.objects.get(id=id)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(NttcsCf20231.objects.all(), 50)
        context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(NttcsCf20231.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):

        page = self.request.GET.get('page', 1)
        paginator = Paginator(NttcsCf20231.objects.all(), 50)
        context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(NttcsCf20231.objects.all())
        return context


# Clase para la pagina de MantenimientoMapeoMarcos
class MantenimientoMapeoMarcos(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoMapeoMarcos.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        if self.request.GET.get('page'):
            consulta = MapeoMarcos.objects.all().values_list('ntt_id', AsociacionMarcos.objects.get(
                marco_id=self.request.session["seleccion"]).nombre_tabla.lower())
            page = self.request.GET.get('page', 1)
            paginator = Paginator(consulta, 50)
            context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
            context["assess"] = AsociacionMarcos.objects.all()
            context["entity"] = paginator.page(page)
            context["paginator"] = paginator  # fijamos la tabla a el valor seleccionado
            context["seleccionado"] = True
            context['marcoSeleccionado'] = self.request.session["seleccion"]
        else:
            context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
            context["assess"] = AsociacionMarcos.objects.all()

            context["lenConsulta"] = 1
            context["seleccionado"] = False
        return context

    # funcion que envia el contexto de la pagina.
    def post(self, request, **knwargs):

        if 'selector' in request.POST:  # if que recoge la pulsacion del boton de seleccion
            selector = request.POST.get('selector')  # guardamos el valor del selecctor de marcos
            if selector == 'None':
                context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
                context["assess"] = AsociacionMarcos.objects.all()
                context["lenConsulta"] = 1
                context["seleccionado"] = False
                return render(request, self.template_name, context=context)
            else:

                consulta = MapeoMarcos.objects.all().values_list('ntt_id', AsociacionMarcos.objects.get(
                    marco_id=selector).nombre_tabla.lower())
                page = request.GET.get('page', 1)
                paginator = Paginator(consulta, 50)
                context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
                context["assess"] = AsociacionMarcos.objects.all()
                context["entity"] = paginator.page(page)
                context["paginator"] = paginator  # fijamos la tabla a el valor seleccionado
                context["lenConsulta"] = 5
                context["seleccionado"] = True
                context['marcoSeleccionado'] = selector
                request.session["seleccion"] = selector  # guardamos la seleecion del marco
                return render(request, self.template_name, context=context)

        elif 'modificar' in request.POST:
            ntt_id = request.POST.get('ntt_id')  # valor del input de ntt_id
            marco = request.POST.get('marco')  # valor del input de marco
            s = AsociacionMarcos.objects.get(marco_id=request.session["seleccion"]).nombre_tabla.lower()

            c = MapeoMarcos.objects.get(ntt_id=ntt_id)
            setattr(c, s, int(marco))
            c.save()


        elif 'eliminar' in request.POST:
            ntt_id = request.POST.get('ntt_id')  # valor del input de ntt_id
            c = MapeoMarcos.objects.get(ntt_id=ntt_id)
            c.delete()



        elif 'insertar' in request.POST:
            ntt_id = request.POST.get('ntt_id')  # valor del input de ntt_id
            marco = request.POST.get('marco')  # valor del input de marco
            if ntt_id != '' and marco != '':
                if not MapeoMarcos.objects.filter(ntt_id=ntt_id).exists():
                    s = AsociacionMarcos.objects.get(marco_id=request.session["seleccion"]).nombre_tabla.lower()
                    c = MapeoMarcos(ntt_id=ntt_id)
                    setattr(c, s, int(marco))
                    c.save()
                else:
                    messages.error(request, 'ERROR,el valor de id ya existe')
            else:
                messages.error(request, 'ERROR, debe introducir todos los valores para insertar un marco')
        elif 'ant' in request.POST:
            if request.session['inicio'] > 0:
                request.session['inicio'] = request.session['inicio']-100
        elif 'sig' in request.POST:
            if request.session['inicio'] < AsociacionMarcos.objects.all().count():
                request.session['inicio'] = request.session['inicio']+100
        consulta = MapeoMarcos.objects.all().values_list('ntt_id', AsociacionMarcos.objects.get(
            marco_id=request.session["seleccion"]).nombre_tabla.lower())
        page = request.GET.get('page', 1)
        paginator = Paginator(consulta, 50)
        context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
        context["assess"] = AsociacionMarcos.objects.all()
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator  # fijamos la tabla a el valor seleccionado
        context["seleccionado"] = True
        context['marcoSeleccionado'] = request.session["seleccion"]
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.


# Clase para la pagina de MantenimientoAssessmentArchivados
class MantenimientoAssessmentArchivados(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoAssessmentArchivados.html"
    
    # funcion que envia el contexto de la pagina.
    def post(self, request, **knwargs):
        if 'selector' in request.POST:  # if que recoge la pulsacion del boton de seleccion
            selector = request.POST.get('selector')  # guardamos el valor del selecctor de marcos
            if selector == 'None':
                context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
                context["assess"] = Assessmentguardados.objects.filter(archivado=1)
                context["seleccionado"] = False
                return render(request, self.template_name, context=context)
            else:
                assGuardado = Assessmentguardados.objects.get(id_assessment=selector)
                  # realizamos la consulta para obtener los contrloles del marco seleccionado
                page = self.request.GET.get('page', 1)
                paginator = Paginator(AssessmentCreados.objects.filter(assessment=assGuardado), 50)
                context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
                context["assess"] = Assessmentguardados.objects.filter(archivado=1)
                context["entity"] = paginator.page(page)
                context["paginator"] = paginator  # fijamos la tabla a el valor seleccionado
                context["seleccionado"] = True
                context['marcoSeleccionado'] = selector
                request.session["seleccion"] = selector
                request.session["seleccionado"] = True
                return render(request, self.template_name, context=context)

        elif 'modificar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            nombre = request.POST.get('nombre')  # valor del input de nombre
            descripcion = request.POST.get('descripcion')  # valor del input de descripcion
            Pregunta = request.POST.get('pregunta')  # valor del input de Pregunta
            criterio = request.POST.get('criterio')  # valor del input de criterio
            respuesta = request.POST.get('respuesta')  # valor del input de respuesta
            valoracion = request.POST.get('valoracion')  # valor del input de respuesta
            valoracionobjetivo = request.POST.get('valoracionobjetivo')  # valor del input de evidencia
            c = AssessmentCreados.objects.get(assessment=request.session.get('seleccion'), control_id=id)
            c.control_name = nombre
            c.descripcion = descripcion
            c.pregunta = Pregunta
            c.criterio = criterio
            c.respuesta = respuesta
            c.valoracion = valoracion
            c.valoracionobjetivo = valoracionobjetivo
            c.save()


        elif 'eliminar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            c = AssessmentCreados.objects.filter(assessment=request.session.get('seleccion'), control_id=id)
            c.delete() # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        elif 'insertar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            nombre = request.POST.get('nombre')  # valor del input de nombre
            descripcion = request.POST.get('descripcion')  # valor del input de descripcion
            Pregunta = request.POST.get('pregunta')  # valor del input de Pregunta
            criterio = request.POST.get('criterio')  # valor del input de criterio
            respuesta = request.POST.get('respuesta')  # valor del input de respuesta
            valoracion = request.POST.get('valoracion')  # valor del input de respuesta
            valoracionobjetivo = request.POST.get('valoracionobjetivo')  # valor del input de evidencia
            if id != '' and descripcion != '' and Pregunta != '' and criterio != '' and respuesta != '' and valoracion != '' and valoracionobjetivo != '':
                if not AssessmentCreados.objects.filter(assessment=request.session.get('seleccion'), control_id=id):
                    a = AssessmentCreados(assessment=request.session.get('seleccion'), control_id=id,
                                          control_name=nombre,
                                          descripcion=descripcion, pregunta=Pregunta,
                                          criteriovaloracion=criterio, valoracionobjetivo=valoracionobjetivo, respuesta=respuesta, valoracion=valoracion)
                    a.save()
                else:
                    messages.error(request, 'ERROR,el valor de id ya existe')
            else:
                messages.error(request, 'ERROR, debe introducir todos los valores para insertar un marco')

        elif 'eliminarAssessment' in request.POST:
            consulta = Assessmentguardados.objects.get(id_assessment=request.session.get('seleccion'))
            consulta.delete()
            return redirect('menu')

        elif 'desarchivar' in request.POST:
            consulta = Assessmentguardados.objects.get(
                id_assessment=request.session.get('seleccion'))  # colsulta para la selecionar el assesment
            consulta.archivado = 0  # ponemos el valor de archivado a 0
            consulta.save()

        assGuardado = Assessmentguardados.objects.get(id_assessment=request.session["seleccion"])
        # realizamos la consulta para obtener los contrloles del marco seleccionado
        page = self.request.GET.get('page', 1)
        paginator = Paginator(AssessmentCreados.objects.filter(assessment=assGuardado), 50)
        context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.filter(archivado=1)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator  # fijamos la tabla a el valor seleccionado
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        if self.request.GET.get('page'):
            assGuardado = Assessmentguardados.objects.get(id_assessment= self.request.session["seleccion"])
            # realizamos la consulta para obtener los contrloles del marco seleccionado
            page = self.request.GET.get('page', 1)
            paginator = Paginator(AssessmentCreados.objects.filter(assessment=assGuardado), 50)
            context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
            context["assess"] = Assessmentguardados.objects.filter(archivado=1)
            context["entity"] = paginator.page(page)
            context["paginator"] = paginator  # fijamos la tabla a el valor seleccionado
            context["seleccionado"] = True
            context['marcoSeleccionado'] = self.request.session["seleccion"]
        else:
            context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
            context["assess"] = Assessmentguardados.objects.filter(archivado=1)
        return context




# DATA TABLES

# clase de prueba codigo python
class MantDominios2(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantDominios2.html"


    def get_context_data(self, **knwargs):
        context = super(MantDominios2, self).get_context_data(**knwargs)
        context["dominios"] = Domains.objects.all()

        return context



    # funcion que envia el contexto de la pagina.

    def post(self, request, **knwargs):

        # insertar datos en la tabla

        if 'insertar' in request.POST:
            identifier = request.POST.get('identifier')
            domain = request.POST.get('domain')
            security = request.POST.get('security')
            principle_intent = request.POST.get('principle_intent')

            insert = Domains(identifier=identifier,
                             domain=domain,
                             security_privacy_by_design_s_p_principles=security,
                             principle_intent=principle_intent,
                             comentario="hola",
                             comentario2="hola comentario 2")
            insert.save()

        # modificar datos en la tabla
        if 'modificar' in request.POST:
            identifier = request.POST.get('identifier')
            domain = request.POST.get('domain')
            security = request.POST.get('security')
            principle_intent = request.POST.get('principle_intent')

            modify = Domains(identifier=identifier)
            modify.domain = domain
            modify.security_privacy_by_design_s_p_principles = security
            modify.principle_intent = principle_intent
            modify.comentario = "comentario modificado"

            modify.save()

        # eliminar datos en la tabla
        if 'eliminar' in request.POST:
            identifier = request.POST.get('identifier')

            borrar = Domains(identifier=identifier)
            borrar.delete()

        # una vez realizado una accion como identificar, eliminar o modificar regresa a mostrar todos los datos.
        context = super(MantDominios2, self).get_context_data(**knwargs)
        context["infoTabla"] = Domains.objects.all()
        return render(request, self.template_name, context=context)




