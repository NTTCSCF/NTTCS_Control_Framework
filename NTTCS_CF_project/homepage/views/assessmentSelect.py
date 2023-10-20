from .__imports__ import *


class assessmentselect(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'assessmentselect' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/assessmentselect.html"

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        '''Asegura que cualquier funcionalidad definida en las clases base 'LoginRequiredMixin' y 'TemplateView'
        se ejecute antes de personalizarla en la subclase assessmentselect.'''
        context = super(assessmentselect, self).get_context_data(**knwargs)
        context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
        context["marcos"] = AsociacionMarcos.objects.all()
        return context

    def post(self, request, **knwargs):
        '''Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        # Valor del input de nombre.
        nombre = request.POST.get('in')
        # Valor del input de codigo.
        codigo = request.POST.get('codigo')
        # Valor de selector de proyecto.
        selectorProyecto = request.POST.get('selectorProyecto')
        # Valor de selector de marcos de seguridad.
        select2 = request.POST.getlist('selector2')
        # Valor del input de idioma.
        idioma = request.POST.get('idioma')
        # Valor asociado al botón de editar (el id del assesmment asociado).
        btnEditar = request.POST.get('btnEditar')
        # Valor asociado al botón de archivar (el id del assesmment asociado).
        btnArchivar = request.POST.get('btnArchivar')

        # Comprueba si el usuario ha seleccionado un proyecto en el formulario.
        if 'selectorProyecto' in request.POST:

            '''Inicialización del contexto '''
            # Esto inicializa un diccionario llamado context con algunos datos de contexto.
            context = super(assessmentselect, self).get_context_data(**knwargs)
            # Añade al conexto los proyectos asociados al usuario.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSelec"] = selectorProyecto
            context["proyectoSeleccionado"] = True
            # Recupera todos los objetos de la classe AsociacionProyectoAssessment filtrados por el proyecto
            # seleccionado en el selector de proyectos.
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=selectorProyecto), assessment__archivado=0)
            # Se guardan todos los marcos de seguridad en el contexto.
            context["marcos"] = AsociacionMarcos.objects.all()

            # Se guarda el proyecto seleccionado en una sessión en el servidor,
            request.session["proyectoSeleccionado"] = selectorProyecto

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se decide editar algún assessments.
        elif 'btnEditar' in request.POST:
            request.session["assessmentGuardado"] = btnEditar

            # Redirección hacia la url especificada en base del nombre.
            return redirect("assessment")

        # Si se presiona el botón 'plan de proyecto' asociado a cada assessment.
        elif 'btnPlan' in request.POST:
            request.session["assessmentGuardado"] = request.POST.get('btnPlan')

            # Redirección hacia la url especificada en base del nombre.
            return redirect("planProyecto")

        # Si se presiona el botón 'archivar' asociado a cada assessment.
        elif 'btnArchivar' in request.POST:

            # Buscamos el assessment en función del id.
            ass = Assessmentguardados.objects.get(id_assessment=btnArchivar)
            # Se archiva el assessment (0 = no archivado / 1 = archivado).
            ass.archivado = 1
            # Se actualiza la fecha en formato 'AAAA-MM-DD'.
            ass.fecha_cierre = datetime.now().isoformat().split('T')[0]
            # Se guardan todos los cambios.
            ass.save()

            '''Inicialización del contexto '''
            # Se inicializa un diccionario llamado context con algunos datos de contexto.
            context = super(assessmentselect, self).get_context_data(**knwargs)
            # Conseguimos los proyectos asociados al usuario.
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSeleccionado"] = True
            # Guardamos en el contexto el proyecto seleccionado, el cual fue guardado anteriormente.
            context["proyectoSelec"] = request.session.get('proyectoSeleccionado')
            # Obtenemos todos los filas de la tabla 'AsociacionProyectoAssessment' que cumplan dichas condiciones.
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session.get('proyectoSeleccionado')),
                assessment__archivado=0)
            # Se guardan todos los marcos de seguridad en el contexto.
            context["marcos"] = AsociacionMarcos.objects.all()

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se escribe algo en el campo de nombre del assessment.
        elif 'in' in request.POST:

            # Si tanto el nombre como el selector de marcos están seleccionados.
            if nombre != '' and select2 != None:
                # Comprobamos que el nombre del assessment no existe en la BD (nombre nuevo)
                if Assessmentguardados.objects.filter(id_assessment=nombre).exists() == False:

                    # Creamos una nueva fila en 'assessmentguardados' inicializada con el nombre del assessment,
                    # la fecha de creación en formato 'AAAA-MM-DD', el idioma y el estado (0 = no archivado).
                    assessmentNuevo = Assessmentguardados(id_assessment=nombre,
                                                          codigo=codigo,
                                                          archivado=0,
                                                          fecha_creacion=datetime.now().isoformat().split('T')[0],
                                                          idioma=idioma,
                                                          estado=1,
                                                          creado=request.user)
                    # Guardamos dicho assessment en la base de datos.
                    assessmentNuevo.save()

                    marcos = ''
                    ''' Marcos de NTT separados por un espacio.'''

                    marc = []
                    '''Lista de marcos de NTT.'''

                    # Iteramos sobre el selector de marcos.
                    for i in select2:
                        # Conseguimos el nombre de la tabla asociada a la iteración.
                        consulta = AsociacionMarcos.objects.get(marco_id=i).nombre_tabla

                        # Accede a la columna ('consulta') y accede a la fila con valor a 1,
                        # que pertenece al marco de NTT correspondiente.
                        c = MapeoMarcos.objects.extra(
                            where=[consulta + "='1'"])

                        # Recorremos la tabla del marco.
                        for fila in c:
                            if fila.ntt_id not in marc:
                                # Guardamos los marcos de NTT sin repetirlos.
                                marc += [fila.ntt_id]

                    for marco in marc:
                        # Añadimos un elemento de la lista al string, separado por un espacio.
                        marcos += marco + '\n'

                        # Obtenemos el assesment en función del idioma y del marco de NTT.
                        if idioma == 'en':
                            consulta = Assessment.objects.get(id=marco)
                        else:
                            consulta = AssessmentEs.objects.get(id=marco)

                        # Manera compacta de guardar muchos campos distintos en una sola variable.
                        # Posteriormente, se usará "split('-33--33-')" para acceder a cada campo.
                        criterioVal = consulta.campo9 + '[-33--33-]' + consulta.campo10 + '[-33--33-]' + consulta.campo11 + '[-33--33-]' + consulta.campo12 + '[-33--33-]' + consulta.campo13 + '[-33--33-]' + consulta.campo14

                        # Se crea una fila en 'AssessmentCreados' y se guarda en la BD.
                        a = AssessmentCreados(assessment=assessmentNuevo, control_id=str(marco),
                                              control_name=consulta.control,
                                              descripcion=consulta.control_description,
                                              pregunta=consulta.control_question,
                                              criteriovaloracion=criterioVal)
                        a.save()

                    # Actualizamos la fila creada anteriormente con los marcos de NTT.
                    assessmentNuevo.marcos = marcos
                    assessmentNuevo.save()

                    # Asociamos el assessment nuevo con el proyecto seleccionado y se guarda en la BD.
                    proyecto = Proyecto.objects.get(codigo=request.session.get('proyectoSeleccionado'))
                    asociacion = AsociacionProyectoAssessment(assessment=assessmentNuevo, proyecto=proyecto)
                    asociacion.save()

                    '''Inicialización del contexto '''
                    # Se inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(assessmentselect, self).get_context_data(**knwargs)
                    # Conseguimos los proyectos asociados al usuario.
                    context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
                    context["proyectoSeleccionado"] = True
                    # Guardamos en el contexto el proyecto seleccionado, el cual fue guardado anteriormente.
                    context["proyectoSelec"] = request.session.get('proyectoSeleccionado')
                    # Obtenemos todos los filas de la tabla 'AsociacionProyectoAssessment' que cumplan dichas condiciones.
                    context["assess"] = AsociacionProyectoAssessment.objects.filter(
                        proyecto=Proyecto.objects.get(codigo=request.session.get('proyectoSeleccionado')),
                        assessment__archivado=0)
                    # Se guardan todos los marcos de seguridad en el contexto.
                    context["marcos"] = AsociacionMarcos.objects.all()

                    # Se renderiza el template en base del contexto.
                    return render(request, self.template_name, context=context)

                # Si el nombre del assessment ya existe en la BD (nombre repetido).
                else:
                    # Mensaje de error.
                    messages.error(request, 'El Assessment ya exsiste.')

                    '''Inicialización del contexto '''
                    # Se inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(assessmentselect, self).get_context_data(**knwargs)
                    # Conseguimos los proyectos asociados al usuario.
                    context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
                    # Guardamos en el contexto el proyecto seleccionado, el cual fue guardado anteriormente.
                    context["proyectoSelec"] = request.session.get('proyectoSeleccionado')
                    context["proyectoSeleccionado"] = True
                    # Obtenemos todos los filas de la tabla 'AsociacionProyectoAssessment' que cumplan dichas condiciones.
                    context["assess"] = AsociacionProyectoAssessment.objects.filter(
                        proyecto=Proyecto.objects.get(codigo=request.session.get('proyectoSeleccionado')),
                        assessment__archivado=0)
                    # Se guardan todos los marcos de seguridad en el contexto.
                    context["marcos"] = AsociacionMarcos.objects.all()

                    # Se renderiza el template en base del contexto.
                    return render(request, self.template_name, context=context)

            # Si tanto el nombre como el selector de marcos están vacíos.
            else:
                # Se crea mensage de error
                messages.error(request, 'Necesitas introducir un nombre para el Assessment')

                '''Inicialización del contexto '''
                # Se inicializa un diccionario llamado context con algunos datos de contexto.
                context = super(assessmentselect, self).get_context_data(**knwargs)
                # Conseguimos los proyectos asociados al usuario.
                context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
                # Guardamos en el contexto el proyecto seleccionado, el cual fue guardado anteriormente.
                context["proyectoSelec"] = request.session.get('proyectoSeleccionado')
                context["proyectoSeleccionado"] = True
                # Obtenemos todos los filas de la tabla 'AsociacionProyectoAssessment' que cumplan dichas condiciones.
                context["assess"] = AsociacionProyectoAssessment.objects.filter(
                    proyecto=Proyecto.objects.get(codigo=request.session.get('proyectoSeleccionado')),
                    assessment__archivado=0)
                # Se guardan todos los marcos de seguridad en el contexto.
                context["marcos"] = AsociacionMarcos.objects.all()

                # Se renderiza el template en base del contexto.
                return render(request, self.template_name, context=context)