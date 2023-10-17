from .__imports__ import *

class entrevistasUsuarios(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'entrevistasUsuarios' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/EntrevistasUsuario.html"

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
        # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
        context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
        # Inicializa la variable de contexto "proyectoSelec" como una cadena vacía.
        context["proyectoSelec"] = ''
        # Filtra y agrega las entrevistas creadas por el usuario actual en el contexto.
        context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
        # Filtra y agrega las asociaciones de entrevistas a las que el usuario actual asiste en el contexto.
        context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

        # Devuelve el contexto con los datos agregados.
        return context

    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario. '''

        # Si se ha seleccionado algún proyecto.
        if 'selectorProyecto' in request.POST:
            # Obtiene el contexto de la superclase con los argumentos proporcionados.
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)

            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectoSelec"] = request.POST.get('selectorProyecto')
            # Se pone a true el 'proyectoSeleccionado' con tal de que se muestre un template de assessment.
            context["proyectoSeleccionado"] = True

            # Almacena el valor del campo 'selectorProyecto' en la sesión actual del usuario.
            request.session["proyectoSeleccionado"] = request.POST.get('selectorProyecto')
            # Se filtra los assessment en base de los diferentes requerimientos.
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.POST.get('selectorProyecto')), assessment__archivado=0)
            # Se guarda todos los marcos de la bd.
            context["marcos"] = AsociacionMarcos.objects.all()
            # Se filtra las diversas entrevistas en base del usuario actual.
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            # Se filtra la tabla 'AsociacionEntrevistasUsuarios' en base del ususario.
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

            # Se renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si el campo 'selectorAssessment' está seleccionado.
        elif 'selectorAssessment' in request.POST:
            # Obtiene el contexto de la superclase con los argumentos proporcionados.
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)

            # Almacena el valor del campo 'proyectoSeleccionado' en la sesión actual del usuario.
            context["proyectoSelec"] = request.session.get('proyectoSeleccionado')
            context["proyectoSeleccionado"] = True
            request.session["proyectoSeleccionado"] = request.session.get('proyectoSeleccionado')

            # Almacena el valor del campo 'selectorAssessment' en la sesión actual del usuario.
            context["assessSelec"] = request.POST.get('selectorAssessment')
            context["assessmentSeleccionado"] = True
            request.session["assessmentSeleccionado"] = request.POST.get('selectorAssessment')

            # Se filtra y agrega los AssessmentCreados asociados al assessment seleccionado al contexto.
            context["controlesAssess"] = AssessmentCreados.objects.filter(
                assessment=request.POST.get('selectorAssessment'))
            # Se filtra y agrega los usuarios asociados al proyecto seleccionado al contexto.
            context["usuarios"] = AsociacionUsuariosProyecto.objects.filter(
                proyecto=request.session.get('proyectoSeleccionado'))
            # Se filtra y agrega los proyectos asociados al proyecto seleccionado que no estén archivados al contexto.
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session["proyectoSeleccionado"]), assessment__archivado=0)
            # Se agrega todos los objetos de AsociacionMarcos al contexto.
            context["marcos"] = AsociacionMarcos.objects.all()
            # Se filtra y agrega las entrevistas creadas por el usuario actual al contexto.
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            # Se filtra y agrega las asociaciones de entrevistas a las que el usuario actual asiste al contexto.
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el campo 'btnEditarEntrevista'.
        elif 'btnEditarEntrevista' in request.POST:
            # Si el campo 'btnEditarEntrevista' está presente en la solicitud POST.
            entrevista = Entrevistas.objects.get(id=request.POST.get('btnEditarEntrevista'))

            # Obtiene el contexto de la superclase con los argumentos proporcionados.
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            # Obtiene y agrega el código del proyecto asociado a la entrevista al contexto.
            context["proyectoSelec"] = AsociacionProyectoAssessment.objects.get(
                assessment=entrevista.assesment).proyecto.codigo
            context["proyectoSeleccionado"] = True

            # Almacena el código del proyecto asociado a la entrevista en la sesión actual del usuario.
            request.session["proyectoSeleccionado"] = AsociacionProyectoAssessment.objects.get(
                assessment=entrevista.assesment).proyecto.codigo

            # Agrega el ID del assessment asociado a la entrevista al contexto.
            context["assessSelec"] = entrevista.assesment.id_assessment
            context["assessmentSeleccionado"] = True

            # Almacena el ID del assessment asociado a la entrevista en la sesión actual del usuario.
            request.session["assessmentSeleccionado"] = entrevista.assesment.id_assessment
            context["entrevistaEditarEditando"] = True

            # Agrega la instancia de la entrevista al contexto.
            context["entrevistaEditar"] = entrevista
            # Agrega la instancia de la entrevista al contexto.
            context["entrevistaEditarConsultores"] = AsociacionEntrevistasUsuarios.objects.filter(
                entrevista=entrevista).values_list("usuario", flat=True)

            # Formatea y agrega la fecha de la entrevista al contexto en formato ISO 8601.
            context["entrevistaEditarFecha"] = entrevista.fecha.replace(tzinfo=None).isoformat(timespec='minutes')
            # Formatea y agrega la duración estimada de la entrevista al contexto en formato ISO 8601.
            context["entrevistaEditarDuracion"] = entrevista.duracionestimada.isoformat(timespec='minutes')
            # Divide los controles de la entrevista por salto de línea y los agrega al contexto.
            context["entrevistaControles"] = entrevista.grupocontroles.split("\n")

            # Filtra y agrega los AssessmentCreados asociados al ID del assessment de la entrevista al contexto.
            context["controlesAssess"] = AssessmentCreados.objects.filter(
                assessment=entrevista.assesment.id_assessment)
            # Filtra y agrega los usuarios asociados al proyecto del assessment de la entrevista al contexto.
            context["usuarios"] = AsociacionUsuariosProyecto.objects.filter(
                proyecto=AsociacionProyectoAssessment.objects.get(assessment=entrevista.assesment).proyecto)
            # Filtra y agrega los proyectos asociados al proyecto del assessment no archivados al contexto.
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=AsociacionProyectoAssessment.objects.get(assessment=entrevista.assesment).proyecto,
                assessment__archivado=0)

            # Agrega todos los objetos de AsociacionMarcos al contexto.
            context["marcos"] = AsociacionMarcos.objects.all()
            # Filtra y agrega las entrevistas creadas por el usuario actual al contexto.
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            # Filtra y agrega las entrevistas creadas por el usuario actual al contexto.
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el botón de 'crear entrevista'.
        elif 'btnCrearEntrevista' in request.POST:
            # Obtiene una lista de los controles seleccionados en el selector.
            controles = request.POST.getlist('selectorControles')
            # Inicializa una cadena vacía para el grupo de controles.
            grupoControles = ''

            # Itera sobre los controles seleccionados y los agrega a la cadena del grupo de controles.
            for i in controles:
                grupoControles += i + '\n'

            # Comprueba si todos los campos obligatorios no están vacíos.
            if request.POST.get('Titulo') != '' \
                and request.POST.get('Fecha') != '' \
                and request.POST.get('Area') != '' \
                and request.POST.get('Duracion') != '' \
                and request.POST.get('selectorEditor') != '' \
                and grupoControles != '':

                # Crea una nueva instancia de Entrevistas con los valores proporcionados en el cuestionario.
                entrevista = Entrevistas(
                    titulo=request.POST.get('Titulo'),
                    fecha=datetime.fromisoformat(request.POST.get('Fecha')),
                    grupocontroles=grupoControles,
                    area=request.POST.get('Area'),
                    creador=User.objects.get(username=request.user),
                    duracionestimada=request.POST.get('Duracion'),
                    assesment= Assessmentguardados.objects.get(id_assessment=request.session.get('assessmentSeleccionado')),
                    editor=User.objects.get(username=request.POST.get('selectorEditor')),
                    asistentes=request.POST.get('Asistentes'))
                # Se guarda en la bd.
                entrevista.save()

                # Obtiene una lista de usuarios seleccionados en la solicitud POST y los asocia a la entrevista.
                users = request.POST.getlist('selectorUsuarios')
                for i in users:
                    usuario = User.objects.get(username=i)
                    asociar = AsociacionEntrevistasUsuarios(entrevista=entrevista, usuario=usuario)
                    asociar.save()

            # Si algún campo esta vacío.
            else:
                # Se crea un mensaje de error.
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            # Obtiene el contexto de la superclase con los argumentos proporcionados.
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            # Filtra y agrega las entrevistas creadas por el usuario actual en el contexto.
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            # Filtra y agrega las asociaciones de entrevistas a las que el usuario actual asiste en el contexto.
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el botón 'btnEditarEntrevistaEnviar'.
        elif 'btnEditarEntrevistaEnviar' in request.POST:
            # Obtiene una lista de los controles seleccionados en el selector.
            controles = request.POST.getlist('selectorControles')
            # Inicializa una cadena vacía para el grupo de controles.
            grupoControles = ''

            # Itera sobre los controles seleccionados y los agrega a la cadena del grupo de controles.
            for i in controles:
                grupoControles += i + '\n'

            # Comprueba si todos los campos obligatorios no están vacíos.
            if request.POST.get('Titulo') != '' \
               and request.POST.get('Fecha') != '' \
               and request.POST.get('Area') != '' \
               and request.POST.get('Duracion') != '' \
               and request.POST.get('selectorEditor') != '' \
               and grupoControles != '':

                # Obtiene la instancia de la entrevista a editar según el ID proporcionado.
                entrevista = Entrevistas.objects.get(id=request.POST.get('btnEditarEntrevistaEnviar'))

                ''' Actualiza los campos de la entrevista con los valores proporcionados en la solicitud POST. '''
                entrevista.titulo = request.POST.get('Titulo')
                entrevista.fecha = datetime.fromisoformat(request.POST.get('Fecha'))
                entrevista.grupocontroles = grupoControles
                entrevista.area = request.POST.get('Area')
                entrevista.creador = User.objects.get(username=request.user)
                entrevista.duracionestimada = request.POST.get('Duracion')
                entrevista.assesment = Assessmentguardados.objects.get(
                    id_assessment=request.session.get('assessmentSeleccionado'))
                entrevista.editor = User.objects.get(username=request.POST.get('selectorEditor'))
                entrevista.asistentes = request.POST.get('Asistentes')
                # Guarda la instancia actualizada de la entrevista en la base de datos.
                entrevista.save()

                # Guarda la instancia actualizada de la entrevista en la base de datos.
                users = request.POST.getlist('selectorUsuarios')
                for i in users:
                    usuario = User.objects.get(username=i)
                    asociar = AsociacionEntrevistasUsuarios(entrevista=entrevista, usuario=usuario)
                    asociar.save()
            # Si algún campo esta vacío.
            else:
                # Se crea un mensaje de error.
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            # Obtiene el contexto de la superclase con los argumentos proporcionados.
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            # Filtra y agrega las entrevistas creadas por el usuario actual en el contexto.
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            # Filtra y agrega las asociaciones de entrevistas a las que el usuario actual asiste en el contexto.
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si el botón 'btnEditarAssesment' es presionado.
        elif 'btnEditarAssesment' in request.POST:
            # Establece la sesión "EntrevistaEditar" con el valor proporcionado.
            request.session["EntrevistaEditar"] = request.POST.get('btnEditarAssesment')

            # Redirige a la vista "encuestaEntrevista".
            return redirect("encuestaEntrevista")

        # Si el botón 'btnEliminarEntrevista' es presionado.
        elif 'btnEliminarEntrevista' in request.POST:
            # Obtiene la instancia de la entrevista a eliminar según el ID proporcionado.
            entrevista = Entrevistas.objects.get(id=request.POST.get('btnEliminarEntrevista'))
            # Elimina la entrevista de la base de datos.
            entrevista.delete()

            # Obtiene el contexto de la superclase con los argumentos proporcionados.
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            # Filtra y agrega los proyectos asociados al usuario actual en el contexto.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            # Establece el campo "proyectoSelec" en vacío en el contexto.
            context["proyectoSelec"] = ''
            # Filtra y agrega las entrevistas creadas por el usuario actual en el contexto.
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            # Filtra y agrega las asociaciones de entrevistas a las que el usuario actual asiste en el contexto.
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)
