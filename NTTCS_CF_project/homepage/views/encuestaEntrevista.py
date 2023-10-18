from .__imports__ import *

class encuestaEntrevista(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'encuestaEntrevista' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/EncuestaEntrevista.html"

    def contextTotal(self, request, select, context):
        ''' Esta función se ha creado con el propósito de evitar la duplicación de código en el proyecto.
        Actualiza el contexto común en todas las páginas.'''

        # Obtiene la sesión "EntrevistaEditar" y la instancia de la entrevista correspondiente.
        entre = self.request.session.get('EntrevistaEditar')
        entrevista = Entrevistas.objects.get(id=entre)

        # Obtiene el ID del assessment y la instancia del assessment guardado asociado a la entrevista.
        assSelect = entrevista.assesment.id_assessment
        assGuardado = entrevista.assesment

        # Divide el grupo de controles de la entrevista y lo almacena en la lista 'e'.
        e = entrevista.grupocontroles.split('\n')
        # Se quita la última posición.
        e = e[:len(e) - 1]

        # Divide el grupo de controles de la entrevista y lo almacena en la lista 'e'.
        context["primero"] = False
        context["ultimo"] = False

        # Comprueba si el índice del elemento 'select' en 'e' es el último o el primero y actualiza el contexto.
        if e.index(select) == len(e) - 1:
            context["ultimo"] = True
        elif e.index(select) == 0:
            context["primero"] = True

        '''Se actualiza el contexto con la lista de elementos del control de entrevista, 
        copiando todos los elementos de 'e'.'''
        context["controlEntrevista"] = e[:len(e)]

        # Se asigna al contexto el valor de 'assSelect'.
        context["NombreAss"] = assSelect

        # Filtra los objetos de la clase 'AssessmentCreados' a través de 'assGuardado'.
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

        # Recupera el objeto 'AssessmentCreados' que coincide con 'assGuardado' y 'select'.
        control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=select)
        context["control"] = control

        # Establece la sesión "controlSelect" con el valor de 'select'.
        self.request.session["controlSelect"] = select

        # Actualiza el contexto con las evidencias genéricas y creadas asociadas al control y al assessment.
        context["evidencias"] = AsociacionEvidenciasGenericas.objects.filter(assessment=control)
        context["evidencias2"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment=control)

        lista = []
        ''' Lista auxiliar creada para guardar las evidencias independientemente de su idioma. '''

        # Comprueba si el idioma del assessment guardado es inglés.
        if assGuardado.idioma == 'en':
            # Se obtiene todas las evidencias genericas (inglés) y se guarda en el contexto.
            context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()

            # Se guarda cada objeto de 'AsociacionEvidenciasGenericas' en la lista auxiliar.
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia]
        else:
            # Se obtiene todas las evidencias genericas (españa) y se guarda en el contexto.
            context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

            # Se guarda cada objeto de 'AsociacionEvidenciasGenericas' en la lista auxiliar.
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia_id_es]

        # Se guarda en el contexto.
        context["listaEvidencias"] = lista

        # Renderiza el template en base del contexto.
        return request, context

    def get_context_data(self, **knwargs):
        ''' El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Obtiene el valor de 'EntrevistaEditar' almacenado en la sesión actual y lo asigna a la variable.
        entre = self.request.session.get('EntrevistaEditar')
        # Recupera la instancia de 'Entrevistas' en base del id obtenido anteriormente.
        entrevista = Entrevistas.objects.get(id=entre)

        # Obtiene el contexto heredado de la superclase 'encuestaEntrevista' y lo asigna a la variable 'context'.
        context = super(encuestaEntrevista, self).get_context_data(**knwargs)
        # Obtiene el ID del assessment asociado a la entrevista y lo asigna a 'assSelect'.
        assSelect = entrevista.assesment.id_assessment
        assGuardado = entrevista.assesment

        # Divide el grupo de controles de la entrevista y lo almacena en la lista 'e'.
        e = entrevista.grupocontroles.split('\n')
        # Se quita la última posición.
        e = e[:len(e) - 1]

        # Asigna la lista 'e' al contexto con la clave 'controlEntrevista'.
        context["controlEntrevista"] = e
        # Establece la clave 'ultimo' en False y la clave 'primero' en True en el contexto.
        context["ultimo"] = False
        context["primero"] = True

        # Asigna el valor de 'assSelect' al contexto con la clave 'NombreAss'.
        context["NombreAss"] = assSelect
        # Filtra los objetos de la clase 'AssessmentCreados' a través de 'assGuardado'.
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        # Consigue el objeto 'AssessmentCreados' en base de los requerimientos.
        control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=e[0])

        lista = []
        ''' Lista auxiliar creada para guardar las evidencias independientemente de su idioma.'''

        # Comprueba si el idioma del assessment guardado es inglés.
        if assGuardado.idioma == 'en':
            # Se obtiene todas las evidencias genericas (inglés) y se guarda en el contexto.
            context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()

            # Se guarda cada objeto de 'AsociacionEvidenciasGenericas' en la lista auxiliar.
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia]
        # Comprueba si el idioma del assessment guardado es español.
        else:
            # Se obtiene todas las evidencias genericas (españa) y se guarda en el contexto.
            context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

            # Se guarda cada objeto de 'AsociacionEvidenciasGenericas' en la lista auxiliar.
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia_id_es]

        # Asigna la lista 'lista' al contexto con la clave 'listaEvidencias'.
        context["listaEvidencias"] = lista
        # Asigna el objeto 'control' al contexto con la clave 'control'.
        context["control"] = control
        # Establece el valor del primer elemento de 'e' en la sesión actual con la clave 'controlSelect'.
        self.request.session["controlSelect"] = e[0]

        # Filtra los objetos de la clase 'AsociacionEvidenciasGenericas' por el campo 'assessment'.
        context["evidencias"] = AsociacionEvidenciasGenericas.objects.filter(assessment=control)
        # Filtra los objetos de la clase 'AsociacionEvidenciasCreadas' por el campo 'id_assessment'.
        context["evidencias2"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment=control)

        # Devuelve el contexto.
        return context


    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        # Obtiene el valor de 'EntrevistaEditar' almacenado en la sesión actual.
        entre = request.session.get('EntrevistaEditar')
        # Utiliza el valor obtenido anteriormente para recuperar la instancia correspondiente de 'Entrevistas'.
        entrevista = Entrevistas.objects.get(id=entre)
        # Accede al campo 'id_assessment' del objeto 'assesment' asociado a 'entrevista' y se guarda.
        assSelect = entrevista.assesment.id_assessment

        select = request.POST.get('selector')
        ''' Valor del selector de control. '''

        flechaIzquierdaButton = request.POST.get('boton2')
        ''' Usado en el 'cuadro de respuesta', representa la flecha izquierda (color azul) que solo está presente
         cuando el control que se esta preguntando no es el primero  '''

        terminarButton = request.POST.get('boton3')
        ''' Usado en el 'cuadro de respuesta', aparece cuando se está preguntando el último control y se da al 
        botón 'Terminar'. Saldrá una alerta de doble confirmación donde se encontrará este botón con el nombre 
        de 'Terminar' (color rojo). '''

        añadirEvidenciaButton = request.POST.get('boton4')
        ''' Botón de 'Añadir evidencia'. '''

        seleccionarEvidenciaButton = request.POST.get('boton5')
        ''' Botón de 'Seleccionar Evidencia'. '''

        flechaDerechaButton = request.POST.get('boton6')
        ''' Usado en el 'cuadro de respuesta', representa la flecha derecha (color azul) que solo está presente
         cuando el control que se esta preguntando no es el último  '''

        guardarButton = request.POST.get('boton7')
        ''' Usado en el 'cuadro de respuesta', representando el botón de 'Guardar'. '''

        btnEliminarEvidencia = request.POST.get('btnEliminarEvidencia')
        ''' Botón de 'eliminar' presente cuando seleccionas una evidencia. '''

        # Comprueba si hay algún control seleccionado.
        if 'selector' in request.POST:
            # Si no hay ningún control seleccionado.
            if select == 'noSel':
                # Recupera la instancia de 'Entrevistas' correspondiente a 'entre' y la asigna a 'entrevista'.
                entrevista = Entrevistas.objects.get(id=entre)

                # Inicializa el contexto.
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)

                # Obtiene el ID del assessment asociado a la entrevista y lo asigna a 'assSelect',
                # así como el objeto de assessment y lo asigna a 'assGuardado'
                assSelect = entrevista.assesment.id_assessment
                assGuardado = entrevista.assesment

                # Divide la cadena de 'grupocontroles' de la entrevista en una lista, separando por saltos de línea.
                e = entrevista.grupocontroles.split('\n')
                # Actualiza el contexto con la lista 'e' excluyendo el último elemento.
                context["controlEntrevista"] = e[:len(e) - 1]
                # Actualiza el contexto con el valor de 'assSelect' bajo la clave 'NombreAss'.
                context["NombreAss"] = assSelect
                # Filtra los objetos de la clase 'AssessmentCreados' a través de los requerimientos declarados.
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
                # Establece el valor de 'noSel' en la sesión actual con la clave 'controlSelect'.
                self.request.session["controlSelect"] = 'noSel'

                # Renderiza el template en base del contexto.
                return render(request, self.template_name, context=context)
            # Si 'select' no es igual a 'noSel', se ejecuta este bloque.
            else:
                # Se inicializa el contexto.
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                # Llama a la función 'contextTotal' para actualizar el contexto y lo asigna a 'request' y 'context'.
                request, context = self.contextTotal(request, select, context)

                # Renderiza el template en base del contexto.
                return render(request, self.template_name, context=context)

        elif flechaIzquierdaButton == 'btn2':  # recogemos la pulsacion del boton de guardar valoracion
            controlSeleccionado = request.session.get('controlSelect')
            if request.session["controlSelect"] != 'noSel':
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                control.respuesta = str(request.POST.get('respuesta'))
                control.valoracion = request.POST.get('valmad')
                control.valoracionobjetivo = request.POST.get('valmadob')
                control.save()
                e = entrevista.grupocontroles.split('\n')
                e = e[:len(e) - 1]
                controlSeleccionado = e[e.index(request.session.get('controlSelect')) + 1]

            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, controlSeleccionado, context)
            return render(request, self.template_name, context=context)

        elif flechaDerechaButton == 'btn6':  # recogemos la pulsacion del boton de guardar valoracion
            controlSeleccionado = request.session.get('controlSelect')
            if request.session["controlSelect"] != 'noSel':
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                control.respuesta = str(request.POST.get('respuesta'))
                control.valoracion = request.POST.get('valmad')
                control.valoracionobjetivo = request.POST.get('valmadob')
                control.save()
                e = entrevista.grupocontroles.split('\n')
                e = e[:len(e) - 1]
                controlSeleccionado = e[e.index(request.session.get('controlSelect')) - 1]

            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, controlSeleccionado, context)
            return render(request, self.template_name, context=context)

        elif guardarButton == 'btn7':  # recogemos la pulsacion del boton de guardar valoracion
            controlSeleccionado = request.session.get('controlSelect')
            if request.session["controlSelect"] != 'noSel':
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                control.respuesta = str(request.POST.get('respuesta'))
                control.valoracion = request.POST.get('valmad')
                control.valoracionobjetivo = request.POST.get('valmadob')
                control.save()
                controlSeleccionado = request.session.get('controlSelect')
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, controlSeleccionado, context)
            return render(request, self.template_name, context=context)

        elif terminarButton == 'btn3':  # recogemos la pulsacion del boton de guardar valoracion
            controlSeleccionado = request.session.get('controlSelect')
            if request.session["controlSelect"] != 'noSel':
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                control.respuesta = str(request.POST.get('respuesta'))
                control.valoracion = request.POST.get('valmad')
                control.valoracionobjetivo = request.POST.get('valmadob')
                control.save()


            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error

            return redirect('entrevistasUsuarios')
        elif añadirEvidenciaButton == 'btn4':  # if encargado de rellenar las evidencias

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
                        context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, context)
                        return render(request, self.template_name, context=context)
                    else:
                        context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, context)
                        messages.error(request,
                                       'EVIDENCIA INCORRECTA: La evidencia introducida ya existe')  # Se crea mensage de error
                        return render(request, self.template_name, context=context)
                else:
                    context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, controlId, context)
                    messages.error(request, 'EVIDENCIA INCORRECTA Necesita introducir un id y una descripcion para la '
                                            'evidencia')  # Se crea mensage de error
                    return render(request, self.template_name, context=context)
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                request, context = self.contextTotal(request, controlId, context)
                return render(request, self.template_name, context=context)

        elif seleccionarEvidenciaButton == 'btn5':  # if encargado de rellenar las evidencias
            if request.session["controlSelect"] != 'noSel':
                selectorEvidencia = request.POST.get('selectorEvidencia')  # valor de el selector de control
                if selectorEvidencia != 'noSel':
                    assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                    control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                            control_id=request.session["controlSelect"])
                    if assGuardado.idioma == 'en':
                        evidencia = Evidencerequestcatalog.objects.get(evidence_request_references=selectorEvidencia)
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia=evidencia, assessment=control)
                        eviGenerica.save()
                    else:
                        evidencia = EvidencerequestcatalogEs.objects.get(evidence_request_references=selectorEvidencia)
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia_id_es=evidencia, assessment=control)
                        eviGenerica.save()
                    assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                    control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                            control_id=request.session["controlSelect"])
                    control.respuesta = str(request.POST.get('respuesta'))
                    control.valoracion = request.POST.get('valmad')
                    control.valoracionobjetivo = request.POST.get('valmadob')
                    control.save()
                    context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], context)
                    return render(request, self.template_name, context=context)
                else:
                    context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], context)
                    messages.error(request,
                                   'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')  # Se crea mensage de error
                    return render(request, self.template_name, context=context)
            else:
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                request, context = self.contextTotal(request, request.session["controlSelect"], context)
                return render(request, self.template_name, context=context)

        elif btnEliminarEvidencia != '':  # if encargado de Eliminar las evidencias
            evidencia = AsociacionEvidenciasGenericas.objects.get(id=btnEliminarEvidencia)
            evidencia.delete()
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session["controlSelect"], context)
            return render(request, self.template_name, context=context)
