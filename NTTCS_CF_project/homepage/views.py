import mimetypes
from typing import Dict, Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from acounts.models import User
from .models import Assessment, MaturirtyTable, AsociacionMarcos, Assessmentguardados, \
    NttcsCf20231, Domains, Evidencerequestcatalog, Evidencias
from django.views.generic import TemplateView
import mysql.connector
from django.contrib import messages
import csv
import xlsxwriter


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
        consulta = Assessment.objects.get(
            id=select)  # consulta para ver la seleccion del despegable de los controles

        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + assSelect)  # consulta de la seleccion del assesment
        context["NombreAss"] = assSelect
        context["assess"] = mycursor
        context["valMad"] = MaturirtyTable.objects.all()  # consulta para el desplegable de la valoracion de madurez

        request.session["controlSelect"] = select

        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + assSelect + " WHERE ID='" + select + "'")
        for fila in mycursor:  # Rellenamos tanto las casillas de respuesta y valoracion
            context["idControl"] = fila[0]
            context["nControl"] = consulta.control
            context["descripcion"] = fila[1]
            context["pregunta"] = fila[2]
            context["respuesta"] = fila[4]
            context["valoracion"] = fila[5]
            context["criterio"] = fila[3].split('\n')

            if fila[6] != None and fila[6] != '':
                evidenciasParaBuscar = fila[6].split('\n')
                evidencias = []
                for i in evidenciasParaBuscar:
                    try:
                        c = Evidencerequestcatalog.objects.get(evidence_request_references=i)
                        evidencias += ['<p>' + c.evidence_request_references + ', ' + c.artifact_description + '</p>']
                    except:
                        c = Evidencias.objects.get(evidencia_id=i)
                        evidencias += [
                            '<p>' + c.evidencia_id + ', ' + c.comentario + ', <a href="' + c.links + '">' + c.links + '</a>' + '</p>']
            else:
                evidencias = ['']

            context["evidencias"] = evidencias
            return request, context

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        assSelect = self.request.session.get('assessmentGuardado')
        context = super(assessment, self).get_context_data(**knwargs)
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + assSelect)
        context["NombreAss"] = assSelect
        context["assess"] = mycursor
        context["valMad"] = MaturirtyTable.objects.all()
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

        if 'selector' in request.POST:  # se recoge la pulsacion del select
            if select == 'noSel':
                context = super(assessment, self).get_context_data(**knwargs)
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = mycursor
                context["valMad"] = MaturirtyTable.objects.all()
                request.session["controlSelect"] = select
                return render(request, self.template_name, context=context)
            else:
                context = super(assessment, self).get_context_data(**knwargs)
                request, context = self.contextTotal(request, select, assSelect, context)
                return render(request, self.template_name, context=context)

        elif boton2 == 'btn2':  # recogemos la pulsacion del boton de guardar valoracion
            if request.session["controlSelect"] != 'noSel':
                consulta = Assessment.objects.get(
                    id=request.session["controlSelect"])  # consulta para consegir los valores del control seleccionado
                query = """UPDATE """ + assSelect + """ SET descripcion='""" + consulta.control_description + """', 
                pregunta='""" + consulta.control_question + """', respuesta='""" + \
                        str(request.POST.get('respuesta')) + """', valoracion='""" + request.POST.get('valmad') + """' 
                        WHERE ID='""" + consulta.id + """';"""  # consulta para rellenar los valores del control
                # seleccionado
                mycursor = self.conn.cursor()
                mycursor.execute(query)
                self.conn.commit()

            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
            context = super(assessment, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session.get('controlSelect'), assSelect, context)
            return render(request, self.template_name, context=context)
        elif boton4 == 'btn4':  # if encargado de rellenar las evidencias

            idEvidencia = request.POST.get('idEvidencia')  # valor del idEvidencia
            descripcionEvidencia = request.POST.get('DescripcionEvidencia')  # valor del DescripcionEvidencia
            linkEvidencia = request.POST.get('linkEvidencia')  # valor del linkEvidencia
            controlId = request.session["controlSelect"]
            consulta = Assessment.objects.get(
                id=request.session["controlSelect"])
            print(controlId)
            if controlId != 'noSel':
                if idEvidencia != '' and descripcionEvidencia != '':  # recogemos la pulsacion de guardar la evidencia
                    if not Evidencias.objects.filter(evidencia_id=idEvidencia, control_id=controlId,
                                                     assessment=Assessmentguardados.objects.get(
                                                         id_assessment=assSelect)).exists():

                        ev = Evidencias(evidencia_id=idEvidencia, comentario=descripcionEvidencia, links=linkEvidencia,
                                        control_id=controlId,
                                        assessment=Assessmentguardados.objects.get(id_assessment=assSelect))
                        ev.save()
                        mycursor = self.conn.cursor(buffered=True)
                        mycursor.execute("SELECT * FROM " + assSelect + " WHERE ID='" + controlId + "'")
                        evidencia = ''
                        for fila in mycursor:
                            evidencia = fila[6]
                        evidencia += '\n' + idEvidencia
                        query = """UPDATE """ + assSelect + """ SET descripcion='""" + consulta.control_description + """', 
                                        pregunta='""" + consulta.control_question + """', respuesta='""" + \
                                str(request.POST.get('respuesta')) + """', valoracion='""" + request.POST.get(
                            'valmad') + """', evidencia='""" + evidencia + """'
                                                WHERE ID='""" + controlId + """';"""  # consulta para rellenar los valores del control seleccionado
                        mycursor = self.conn.cursor()
                        mycursor.execute(query)
                        self.conn.commit()
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, assSelect, context)
                        return render(request, self.template_name, context=context)
                    else:
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, assSelect, context)
                        messages.error(request,
                                       'EVIDENCIA INCORRECTA: La evidencia introducida ya existe para este control y assessment')  # Se crea mensage de error
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
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + assSelect)
                context["NombreAss"] = assSelect
                context["assess"] = mycursor
                context["valMad"] = MaturirtyTable.objects.all()
                return render(request, self.template_name, context=context)

        else:  # se recoge la pulsacion del boton de archivar tras la confirmacion

            consulta = Assessmentguardados.objects.get(
                id_assessment=assSelect)  # colsulta para la selecionar el assesment
            consulta.archivado = 1  # ponemos el valor de archivado a 1
            consulta.save()
            return redirect('menu')  # volvemos al menu

        context = super(assessment, self).get_context_data(**knwargs)
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + assSelect)
        context["NombreAss"] = assSelect
        context["assess"] = mycursor
        return render(request, self.template_name, context=context)


# Clase para la pagina de AssessmentSelect

class assessmentselect(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/assessmentselect.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')  # constante para la conexion con la base de datos

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

        if 'selector1' in request.POST:
            request.session["assessmentGuardado"] = select
            return redirect("assessment")

        elif nombre != '' and select2 != None:
            query = '''CREATE TABLE ''' + nombre + ''' (
                                ID varchar(100) NOT NULL,
                                descripcion text NULL,
                                pregunta text NULL,
                                criterioValoracion text NULL,
                                respuesta text NULL,
                                valoracion text NULL,
                                evidencia text NULL,
                                CONSTRAINT NewTable_pk PRIMARY KEY (ID)
                            )
                            ENGINE=InnoDB
                            DEFAULT CHARSET=utf8mb4
                            COLLATE=utf8mb4_0900_ai_ci;'''  # query para la creacion de la tabla para uardar el assessment
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute(query)

            marcos = ''
            marc = []
            mycursor = self.conn.cursor(buffered=True)
            for i in select2:  # recorremos el segundo selector

                mycursor.execute("SELECT * FROM " + AsociacionMarcos.objects.get(
                    marco_id=i).nombre_tabla)  # query para seleccionar la tabla del marco seleccionado
                for fila in mycursor:
                    if fila[0] not in marc:
                        marc += [fila[
                                     0]]  # recorremos la tabla del marco cogiendo los controles de ntt que no este repetidos

            for marco in marc:
                marcos += marco + '\n'  # creamos un string con todos los controles de ntt separados por intros
                mycursor = self.conn.cursor(buffered=True)
                consulta = Assessment.objects.get(id=marco)
                criterioVal = consulta.campo9 + '\n' + consulta.campo10 + '\n' + consulta.campo11 + '\n' + consulta.campo12 + '\n' + consulta.campo13 + '\n' + consulta.campo14
                if consulta.evidence_request_references != None:
                    evidencia = consulta.evidence_request_references
                else:
                    evidencia = ''
                query = '''INSERT INTO ''' + nombre + '''(ID, descripcion, pregunta, criterioValoracion, respuesta, 
                    valoracion, evidencia) VALUES("''' + str(
                    marco) + '''", "''' + consulta.control_description.replace('"',
                                                                               "'") + '''", "''' + consulta.control_question.replace(
                    '"', "'") + '''", 
                    "''' + criterioVal.replace('"', "'") + '''", "", "", "''' + evidencia + '''");'''  # query
                # para insertar en la tabla del assessment creado, todos los controles de ntt
                mycursor.execute(query)

            self.conn.commit()
            c = Assessmentguardados(id_assessment=nombre, marcos=marcos,
                                    archivado=0)  # creamos una nueva fila en assessmentguardados con el string de marcos y el nombre del marco
            c.save()

            request.session["assessmentGuardado"] = nombre
            return redirect("assessment")
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
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + selector)  # consulta de la seleccion del assesment

        valores = []
        for fila in mycursor:  # Rellenamos tanto las casillas de respuesta y valoracion

            if fila[6] != None and fila[6] != '':
                evidenciasParaBuscar = fila[6].split('\n')
                evidencias = ''
                for i in evidenciasParaBuscar:
                    try:
                        c = Evidencerequestcatalog.objects.get(evidence_request_references=i)
                        evidencias += c.evidence_request_references + ', ' + c.artifact_description + '\n'
                    except:
                        c = Evidencias.objects.get(evidencia_id=i)
                        evidencias += c.evidencia_id + ', ' + c.comentario + ', ' + c.links + '\n'
            else:
                evidencias = ''

            consulta = Assessment.objects.get(id=fila[0])
            valores += {
                'idControl': fila[0],
                'nControl': consulta.control,
                'descripcion': fila[1],
                'pregunta': fila[2],
                'respuesta': fila[4],
                'valoracion': fila[5],
                'criterio': fila[3],
                'evidencias': evidencias
            },

        titulos = ["idControl", "nControl", "descripcion", "pregunta", "respuesta", "valoracion", "criterio",
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
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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
            Percentage = request.POST.get('Percentage')  # valor del input de percentaje
            insert = MaturirtyTable(ccmmcod=Ccmmcod, description=Description, sublevels=Sublevels,
                                    percentage=Percentage)  # creamos un nuevo input en la tabla
            insert.save()
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

        context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
        context["consulta"] = MaturirtyTable.objects.all()
        context["lenConsulta"] = len(MaturirtyTable.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
        context["consulta"] = MaturirtyTable.objects.all()
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
            insert = Domains(identifier=identifier, domain=domain,
                             security_privacy_by_design_s_p_principles=security_privacy_by_design_s_p_principles,
                             principle_intent=principle_intent, )  # creamos un nuevo input en la tabla
            insert.save()
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

        context = super(MantenimientoDominios, self).get_context_data(**knwargs)
        context["consulta"] = Domains.objects.all()
        context["lenConsulta"] = len(Domains.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoDominios, self).get_context_data(**knwargs)
        context["consulta"] = Domains.objects.all()
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
            insert = Evidencerequestcatalog(evidence_request_references=evidence_request_references,
                                            area_of_focus=area_of_focus, artifact=artifact,
                                            artifact_description=artifact_description,
                                            control_mappings=control_mappings)  # creamos un nuevo input en la tabla
            insert.save()
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
            evidence_request_references = request.POST.get('evidence_request_references')  # valor del input de evidence_request_references

            consulta = Evidencerequestcatalog.objects.get(evidence_request_references=evidence_request_references)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
        context["consulta"] = Evidencerequestcatalog.objects.all()
        context["lenConsulta"] = len(Evidencerequestcatalog.objects.all())
        return render(request, self.template_name,context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
        context["consulta"] = Evidencerequestcatalog.objects.all()
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
            insert = Assessment(id=id, control_question=control_question,
                                control_description=control_description)  # creamos un nuevo input en la tabla
            insert.save()
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

        context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
        context["consulta"] = Assessment.objects.all()
        context["lenConsulta"] = len(Assessment.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
        context["consulta"] = Assessment.objects.all()
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

            insert = AsociacionMarcos(marco_id=marco_id,
                                      nombre_tabla=nombre_tabla)  # creamos un nuevo input en la tabla
            insert.save()
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

        context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
        context["consulta"] = AsociacionMarcos.objects.all()
        context["lenConsulta"] = len(AsociacionMarcos.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
        context["consulta"] = AsociacionMarcos.objects.all()
        context["lenConsulta"] = len(AsociacionMarcos.objects.all())
        return context

    # Funcion utilizada para eliminar el valor seleccionado de la tabla


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
            insert = NttcsCf20231(domain=domain, selected_y_n_field=selected_y_n_field, id=id, control=control,
                                  control_description=control_description,
                                  relative_control_weighting=relative_control_weighting,
                                  function_grouping=function_grouping, assesed_result=assesed_result,
                                  numeric_result=numeric_result, weighted_numeric_result=weighted_numeric_result,
                                  assessment_comments=assessment_comments,
                                  relative_result_by_function=relative_result_by_function,
                                  relative_result_by_domain=relative_result_by_domain)  # creamos un nuevo input en la tabla
            insert.save()
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

        context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
        context["consulta"] = NttcsCf20231.objects.all()
        context["lenConsulta"] = len(NttcsCf20231.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
        context["consulta"] = NttcsCf20231.objects.all()
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
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + AsociacionMarcos.objects.get(
                    marco_id=selector).nombre_tabla)  # realizamos la consulta para obtener los contrloles del marco seleccionado
                context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
                context["assess"] = AsociacionMarcos.objects.all()
                context["consulta"] = mycursor  # fijamos la tabla a el valor seleccionado
                context["lenConsulta"] = 5
                context["seleccionado"] = True
                context['marcoSeleccionado'] = selector
                request.session["seleccion"] = AsociacionMarcos.objects.get(
                    marco_id=selector).nombre_tabla  # guardamos la seleecion del marco
                return render(request, self.template_name, context=context)

        elif 'modificar' in request.POST:
            ntt_id = request.POST.get('ntt_id')  # valor del input de ntt_id
            marco = request.POST.get('marco')  # valor del input de marco
            id = request.POST.get('id')  # valor del input de id

            query = "UPDATE " + request.session["seleccion"] + " SET NTT_ID='" + ntt_id + "', " + request.session[
                "seleccion"] + "='" + marco + "' WHERE ID=" + id + ";"  # si esta en la tabla seleccionamos el ojeto en la tabla
            mycursor = self.conn.cursor()
            mycursor.execute(query)
            self.conn.commit()


        elif 'eliminar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute(
                "DELETE FROM " + request.session["seleccion"] + " WHERE ID='" + id + "';")
            self.conn.commit()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.


        elif 'insertar' in request.POST:
            ntt_id = request.POST.get('ntt_id')  # valor del input de ntt_id
            marco = request.POST.get('marco')  # valor del input de marco

            query = "INSERT INTO " + request.session["seleccion"] + " (NTT_ID, " + request.session[
                "seleccion"] + ") VALUES('" + ntt_id + "', '" + marco + "');"  # creamos un nuevo input en la tabla
            mycursor = self.conn.cursor()
            mycursor.execute(query)
            self.conn.commit()

        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + request.session["seleccion"])
        context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
        context["assess"] = AsociacionMarcos.objects.all()
        context["consulta"] = mycursor
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.


# Clase para la pagina de MantenimientoAssessmentArchivados
class MantenimientoAssessmentArchivados(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoAssessmentArchivados.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    # funcion que envia el contexto de la pagina.
    def post(self, request, **knwargs):
        if 'selector' in request.POST:  # if que recoge la pulsacion del boton de seleccion
            selector = request.POST.get('selector')  # guardamos el valor del selecctor de marcos
            if selector == 'None':
                context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
                s = Assessmentguardados.objects.get(archivado=1)
                try:
                    len(s)
                    p = s
                except:
                    p = [s]
                context["assess"] = p
                context["seleccionado"] = False
                return render(request, self.template_name, context=context)
            else:
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + selector)  # realizamos la consulta para obtener los contrloles
                # del marco seleccionado
                context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
                s = Assessmentguardados.objects.get(archivado=1)
                try:
                    len(s)
                    p = s
                except:
                    p = [s]
                context["assess"] = p
                context["consulta"] = mycursor  # fijamos la tabla a el valor seleccionado
                context["seleccionado"] = True
                context['marcoSeleccionado'] = selector
                request.session["seleccion"] = selector
                return render(request, self.template_name, context=context)

        elif 'modificar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            descripcion = request.POST.get('descripcion')  # valor del input de descripcion
            Pregunta = request.POST.get('pregunta')  # valor del input de Pregunta
            criterio = request.POST.get('criterio')  # valor del input de criterio
            respuesta = request.POST.get('respuesta')  # valor del input de respuesta
            valoracion = request.POST.get('valoracion')  # valor del input de respuesta
            evidencia = request.POST.get('evidencia')  # valor del input de evidencia

            query = """UPDATE """ + request.session["seleccion"] + """ SET descripcion='""" + descripcion + """', 
                                        pregunta='""" + Pregunta + """', criterioValoracion='""" + criterio + """', 
                                        respuesta='""" + \
                    respuesta + """', valoracion='""" + valoracion + """', 
                                                evidencia='""" + evidencia + """' WHERE ID='""" + id + """';"""  # si
            # esta en la tabla seleccionamos el ojeto en la tabla
            mycursor = self.conn.cursor()
            mycursor.execute(query)
            self.conn.commit()


        elif 'eliminar' in request.POST:
            id = request.POST.get('id')  # valor del input de id

            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute(
                "DELETE FROM " + request.session["seleccion"] + " WHERE ID='" + id + "';")
            self.conn.commit()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.


        elif 'insertar' in request.POST:
            id = request.POST.get('id')  # valor del input de id
            descripcion = request.POST.get('descripcion')  # valor del input de descripcion
            Pregunta = request.POST.get('pregunta')  # valor del input de Pregunta
            criterio = request.POST.get('criterio')  # valor del input de criterio
            respuesta = request.POST.get('respuesta')  # valor del input de respuesta
            valoracion = request.POST.get('valoracion')  # valor del input de respuesta
            evidencia = request.POST.get('evidencia')  # valor del input de evidencia

            query = """INSERT INTO """ + request.session[
                "seleccion"] + """(ID, descripcion, pregunta, criterioValoracion, respuesta, valoracion, 
                                evidencia) VALUES('""" + id + """', '""" + descripcion + """', '""" + Pregunta + """', 
                                '""" + criterio + """', '""" + respuesta + """', '""" + valoracion + """', '""" + evidencia + \
                    """');"""  # creamos un nuevo input en la tabla
            mycursor = self.conn.cursor()
            mycursor.execute(query)
            self.conn.commit()

        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + request.session["seleccion"])
        context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
        s = Assessmentguardados.objects.get(archivado=1)
        try:
            len(s)
            p = s
        except:
            p = [s]
        context["assess"] = p
        context["consulta"] = mycursor
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
        s = Assessmentguardados.objects.get(archivado=1)
        try:
            len(s)
            p = s
        except:
            p = [s]
        context["assess"] = p

        return context

    # Funcion utilizada para eliminar el valor seleccionado de la tabla
    def EliminarAssessment(request):
        conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                       auth_plugin='mysql_native_password')
        mycursor = conn.cursor(buffered=True)
        mycursor.execute(
            "DELETE FROM " + request.session["seleccion"] + " WHERE ID='" + request.session["ultBusqueda"] + "';")
        conn.commit()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.
        return redirect('MantenimientoAssessmentArchivados')


# clase de prueba codigo python
class MantDominios2(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantDominios2.html"

    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    # clase para mostrar datos de la tabla
    def get_context_data(self, **knwargs):
        context = super(MantDominios2, self).get_context_data(**knwargs)
        context["consulta"] = Domains.objects.all()
        # print(Domains.objects.get(identifier="NTT-AAT"))
        # print(Domains.objects.all())
        context["lenConsulta"] = len(Domains.objects.all())
        return context

    def post(self, request, **knwargs):

        # PARA BUSQUEDA EN LA TABLA
        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')
            # consulta2 = Domains.objects.get(identifier=busqueda)

            if busqueda == '':
                context = super(MantDominios2, self).get_context_data(**knwargs)
                context["consulta"] = Domains.objects.all()
                context["lenConsulta"] = len(Domains.objects.all())
                return render(request, self.template_name, context=context)



            else:
                try:
                    consulta = Domains.objects.get(identifier=busqueda)
                    context = super(MantDominios2, self).get_context_data(**knwargs)
                    context.update({'consulta': consulta})
                    context["lenConsulta"] = 1
                    request.session["ultBusqueda"] = busqueda  # fijamos el valor de la ultima busqueda.
                    return render(request, self.template_name, context=context)
                except:
                    context = super(MantDominios2, self).get_context_data(**knwargs)
                    context["consulta"] = Domains.objects.all()
                    context["lenConsulta"] = len(Domains.objects.all())
                    return render(request, self.template_name, context=context)

        # PARA INSERTAR DATOS
        elif request.POST.get('identifier') is not None:
            identifier = request.POST.get('identifier')
            domain = request.POST.get('domain')
            security_privacy_by_design_s_p_principles = request.POST.get('security_privacy_by_design_s_p_principles')
            principle_intent = request.POST.get('principle_intent')

            # verifica que si existe en la BD, en caso que si, se puede modificar la informacion
            try:  # con este try comprobamos si lo que queremos insertar esta en la tabla.
                consulta = Domains.objects.get(
                    identifier=identifier)  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
                consulta.domain = domain
                consulta.security_privacy_by_design_s_p_principles = security_privacy_by_design_s_p_principles
                consulta.principle_intent = principle_intent
                consulta.save()  # fijamos los valores y los guardamos.

            # guarda un registro nuevo
            except:  # si el valor no esta en la tabla
                insert = Domains(identifier=identifier, domain=domain,
                                 security_privacy_by_design_s_p_principles=security_privacy_by_design_s_p_principles,
                                 principle_intent=principle_intent, )  # creamos un nuevo input en la tabla
                insert.save()

            # volvemos a mostrar todos los datos de la tabla
            context = super(MantDominios2, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            return render(request, self.template_name,
                          context=context)  # siempre retornamos el valor con la tabla completa.

        # boton modificar es para rellenar datos en las cajas de texto con la información
        else:
            consulta = Domains.objects.get(identifier=request.session["ultBusqueda"])
            context = super(MantDominios2, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            context[
                "seleccion"] = consulta  # pasamos la consulta para que se rellenen los input con el valor de la ultima seleccion.
            return render(request, self.template_name, context=context)


class MantDom3(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantDom3.html"


"""
            else:  # else que recoge la pulsacion del boton de modificar.
            consulta = Domains.objects.get(identifier=request.session[
                "ultBusqueda"])  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
            context = super(MantenimientoDominios, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            context[
                "seleccion"] = consulta  # pasamos la consulta para que se rellenen los input con el valor de la ultima seleccion.
            return render(request, self.template_name, context=context)
            """

"""
    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:  # if que recoge la pulsacion del boton de busqueda
            busqueda = request.POST.get('busqueda')  # guardamos el valor del input de busqueda

            if busqueda == '':  # detectamos si el valor del buscador esta vacio
                context = super(MantenimientoDominios, self).get_context_data(**knwargs)
                context["consulta"] = Domains.objects.all()  # pasamos el valor de la tabla completa
                context["lenConsulta"] = len(Domains.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = Domains.objects.get(identifier=busqueda)  # consultamos el valor buscado en la tabla
                context = super(MantenimientoDominios, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})  # pasamos la consulta para que se muestre en la tabla
                context["lenConsulta"] = 1  # pasamos la longitud de la consulta.
                request.session["ultBusqueda"] = busqueda  # fijamos el valor de la ultima busqueda.
                return render(request, self.template_name, context=context)

        elif request.POST.get('identifier') is not None:  # if que recoge la pulsacion del boton de insertar.
            identifier = request.POST.get('identifier')  # valor del input de identifier
            domain = request.POST.get('domain')  # valor del input de domain
            security_privacy_by_design_s_p_principles = request.POST.get('security_privacy_by_design_s_p_principles')  # valor del input de security_privacy_by_design_s_p_principles
            principle_intent = request.POST.get('principle_intent')  # valor del input de principle_intent

            try:  # con este try comprobamos si lo que queremos insertar esta en la tabla.
                consulta = Domains.objects.get(identifier=identifier)  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
                consulta.domain = domain
                consulta.security_privacy_by_design_s_p_principles = security_privacy_by_design_s_p_principles
                consulta.principle_intent = principle_intent
                consulta.save()  # fijamos los valores y los guardamos.

            except:  # si el valor no esta en la tabla
                insert = Domains(identifier=identifier, domain=domain,
                                 security_privacy_by_design_s_p_principles=security_privacy_by_design_s_p_principles,
                                 principle_intent=principle_intent, )  # creamos un nuevo input en la tabla
                insert.save()

            context = super(MantenimientoDominios, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            return render(request, self.template_name, context=context)  # siempre retornamos el valor con la tabla completa.

        else:  # else que recoge la pulsacion del boton de modificar.
            consulta = Domains.objects.get(identifier=request.session["ultBusqueda"])  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
            context = super(MantenimientoDominios, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            context["seleccion"] = consulta  # pasamos la consulta para que se rellenen los input con el valor de la ultima seleccion.
            return render(request, self.template_name, context=context)
            """
