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

        entre = request.session.get('EntrevistaEditar')
        ''' Obtiene el valor de 'EntrevistaEditar' almacenado en la sesión actual.'''

        entrevista = Entrevistas.objects.get(id=entre)
        ''' Utiliza el valor obtenido anteriormente para recuperar la instancia correspondiente de 'Entrevistas'.'''

        assSelect = entrevista.assesment.id_assessment
        ''' Accede al campo 'id_assessment' del objeto 'assesment' asociado a 'entrevista' y se guarda.'''

        select = request.POST.get('selector')
        ''' Valor del selector de control. '''

        flechaIzquierdaButton = request.POST.get('boton6')
        ''' Usado en el 'cuadro de respuesta', representa la flecha izquierda (color azul) que solo está presente
         cuando el control que se esta preguntando no es el primero.  '''

        terminarButton = request.POST.get('boton3')
        ''' Usado en el 'cuadro de respuesta', aparece cuando se está preguntando el último control y se da al 
        botón 'Terminar'. Saldrá una alerta de doble confirmación donde se encontrará este botón con el nombre 
        de 'Terminar' (color rojo). '''

        añadirEvidenciaButton = request.POST.get('boton4')
        ''' Botón de 'Añadir evidencia'. '''

        seleccionarEvidenciaButton = request.POST.get('boton5')
        ''' Botón de 'Seleccionar Evidencia'. '''

        flechaDerechaButton = request.POST.get('boton2')
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

        # Si se da al botón con forma de 'flecha derecha' en el cuadro de 'respuesta'.
        elif flechaDerechaButton == 'btn2':
            # Obtiene el valor de 'controlSelect' almacenado en la sesión actual.
            controlSeleccionado = request.session.get('controlSelect')

            # Si hay algún control seleccionado.
            if request.session["controlSelect"] != 'noSel':
                # Obtiene la instancia de 'Assessmentguardados' en base de 'assSelect'.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                # Obtiene la instancia de 'AssessmentCreados' correspondiente a 'assGuardado' y a 'controlSelect'.
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])

                # Asigna los valores de 'respuesta'.
                control.respuesta = str(request.POST.get('respuesta'))
                # Asigna los valores de 'valoración'.
                control.valoracion = request.POST.get('valmad')
                # Asigna los valores de 'valoración objetivo'.
                control.valoracionobjetivo = request.POST.get('valmadob')
                # Se guarda en la bd.
                control.save()

                # Divide la cadena 'grupocontroles' de la entrevista en una lista, separando por saltos de línea.
                e = entrevista.grupocontroles.split('\n')
                # Exluye el último elemento.
                e = e[:len(e) - 1]

                ''' Actualiza 'controlSeleccionado' según el próximo control en 'e' 
                respecto al control seleccionado actualmente en la sesión. '''
                controlSeleccionado = e[e.index(request.session.get('controlSelect')) + 1]

            # Si no se seleccionado ningún control.
            else:
                # Se crea el mensaje de error correspondiente.
                messages.error(request,
                            'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

            # Se inicializa el contexto.
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            # Se actualiza el contexto.
            request, context = self.contextTotal(request, controlSeleccionado, context)

            # Renderiza el template en función del contexto.
            return render(request, self.template_name, context=context)

        # Si se da al botón con forma de 'flecha izquierda' en el cuadro de 'respuesta'.
        elif flechaIzquierdaButton == 'btn6':
            # Obtiene el valor de 'controlSelect' almacenado en la sesión actual.
            controlSeleccionado = request.session.get('controlSelect')

            # Si hay algún control seleccionado.
            if request.session["controlSelect"] != 'noSel':
                # Obtiene la instancia de 'Assessmentguardados' en base de 'assSelect'.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                # Obtiene la instancia de 'AssessmentCreados' correspondiente a 'assGuardado' y a 'controlSelect'.
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])

                # Asigna los valores de 'respuesta'.
                control.respuesta = str(request.POST.get('respuesta'))
                # Asigna los valores de 'valoración'.
                control.valoracion = request.POST.get('valmad')
                # Asigna los valores de 'valoración objetivo'.
                control.valoracionobjetivo = request.POST.get('valmadob')
                # Se guarda en la bd.
                control.save()

                # Divide la cadena 'grupocontroles' de la entrevista en una lista, separando por saltos de línea.
                e = entrevista.grupocontroles.split('\n')
                # Exluye el último elemento.
                e = e[:len(e) - 1]

                ''' Actualiza 'controlSeleccionado' según el anterior control en 'e' 
                respecto al control seleccionado actualmente en la sesión. '''
                controlSeleccionado = e[e.index(request.session.get('controlSelect')) - 1]

            # Si no hay ningún control seleccionado.
            else:
                # Se crea el mensaje de error correspondiente.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

            # Se inicializa el contexto.
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            # Se actualiza el contexto.
            request, context = self.contextTotal(request, controlSeleccionado, context)

            # Se renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el botón de 'guardar'.
        elif guardarButton == 'btn7':
            # Obtiene el valor de 'controlSelect' almacenado en la sesión actual.
            controlSeleccionado = request.session.get('controlSelect')

            # Si hay algún control seleccionado.
            if request.session["controlSelect"] != 'noSel':
                # Obtiene la instancia de 'Assessmentguardados' en base de 'assSelect'.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                # Obtiene la instancia de 'AssessmentCreados' correspondiente a 'assGuardado' y a 'controlSelect'.
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                # Asigna los valores de 'respuesta'.
                control.respuesta = str(request.POST.get('respuesta'))
                # Asigna los valores de 'valoración'.
                control.valoracion = request.POST.get('valmad')
                # Asigna los valores de 'valoración objetivo'.
                control.valoracionobjetivo = request.POST.get('valmadob')
                # Se guarda el control en la BD.
                control.save()

                # TODO: Useless statement?
                controlSeleccionado = request.session.get('controlSelect')

            # Si no hay ningún control seleccionado.
            else:
                # Se crea un mensaje de error.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

            # Se inicialza el contexto.
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            # Se actualiza el contexto.
            request, context = self.contextTotal(request, controlSeleccionado, context)

            # Se renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el botón de 'terminar'.
        elif terminarButton == 'btn3':

            # Si se ha seleccionado algún control.
            if request.session["controlSelect"] != 'noSel':
                # Obtiene la instancia de 'Assessmentguardados' en base de 'assSelect'.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                # Obtiene la instancia de 'AssessmentCreados' correspondiente a 'assGuardado' y a 'controlSelect'.
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])

                # Asigna los valores de 'respuesta'.
                control.respuesta = str(request.POST.get('respuesta'))
                # Asigna los valores de 'valoración'.
                control.valoracion = request.POST.get('valmad')
                # Asigna los valores de 'valoración objetivo'.
                control.valoracionobjetivo = request.POST.get('valmadob')
                # Guarda el control en la BD.
                control.save()
                # Obtiene el valor de 'EntrevistaEditar' almacenado en la sesión actual y lo asigna a la variable.
                entre = self.request.session.get('EntrevistaEditar')
                # Recupera la instancia de 'Entrevistas' en base del id obtenido anteriormente.
                entrevista = Entrevistas.objects.get(id=entre)
                entrevista.terminada=1
                entrevista.save()
            # Si no se ha seleccionado ningun control.
            else:
                # Se genera el menaje de error correspondiente.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

            # Se redirige al usuario hacia /entrevistasUsuarios.
            return redirect('entrevistasUsuarios')

        # Si se presiona el botón de 'añadir evidencia' en el cuadro de 'nueva evidencia'.
        elif añadirEvidenciaButton == 'btn4':

            idEvidencia = request.POST.get('idEvidencia') + '-C'
            ''' Valor del id de la evidencia.'''
            descripcionEvidencia = request.POST.get('DescripcionEvidencia')
            ''' Descripción de la evidencia. '''
            linkEvidencia = request.POST.get('linkEvidencia')
            ''' Link de la evidencia. '''

            # Se consigue el id del control seleccionado a partir de la sessión actual.
            controlId = request.session["controlSelect"]

            # Si hay algún control seleccionado.
            if controlId != 'noSel':
                # Comprueba que los campos 'idEvidencia' y 'descripcionEvidencia' no estén vacíos.
                if idEvidencia != '' and descripcionEvidencia != '':
                    # Verifica si no existe una instancia de 'Evidencias' con 'evidencia_id' igual a 'idEvidencia'.
                    if not Evidencias.objects.filter(evidencia_id=idEvidencia).exists():

                        # Crea una instancia de 'Evidencias' con los valores dados y la guarda en la base de datos.
                        ev = Evidencias(evidencia_id=idEvidencia, comentario=descripcionEvidencia, links=linkEvidencia,
                                        control_id=controlId,
                                        assessment=Assessmentguardados.objects.get(id_assessment=assSelect))
                        # Lo guarda en la BD.
                        ev.save()

                        # Obtiene las instancias de 'Assessmentguardados' y 'AssessmentCreados'.
                        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                        control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                control_id=request.session["controlSelect"])

                        # Asigna los valores de 'respuesta'.
                        control.respuesta = str(request.POST.get('respuesta'))
                        # Asigna los valores de 'valoración'.
                        control.valoracion = request.POST.get('valmad')
                        # Asigna los valores de 'valoración objetivo'.
                        control.valoracionobjetivo = request.POST.get('valmadob')

                        # Crea una instancia 'AsociacionEvidenciasCreadas' en base a los requerimientos.
                        evidencia = AsociacionEvidenciasCreadas(id_evidencia=ev, id_assessment=control)
                        # Se guarda la evidencia en la bd.
                        evidencia.save()

                        # Se inicializa el contexto.
                        context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                        # Se actualiza el contexto.
                        request, context = self.contextTotal(request, controlId, context)

                        # Renderiza el template en base del contexto.
                        return render(request, self.template_name, context=context)

                    # Si existe la evidencia en la bd.
                    else:
                        # Se inicializa el contexto.
                        context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                        # Se actualiza el contexto.
                        request, context = self.contextTotal(request, controlId, context)

                        # Se genera el mensaje de error correspondiente.
                        messages.error(request,
                                       'EVIDENCIA INCORRECTA: La evidencia introducida ya existe')

                        # Renderiza el template en base del contexto.
                        return render(request, self.template_name, context=context)

                # Si los campos 'idEvidencia' y 'descripcionEvidencia' están vacíos.
                else:
                    # Se inicializa el contexto.
                    context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                    # Se actualiza el contexto.
                    request, context = self.contextTotal(request, controlId, context)

                    # Se genera el mensaje de error correspondiente.
                    messages.error(request, 'EVIDENCIA INCORRECTA Necesita introducir un id y una descripcion para la '
                                            'evidencia')

                    # Renderiza el template en base del contexto.
                    return render(request, self.template_name, context=context)

            # Si no se ha seleccionado ningún contexto.
            else:
                # Se genera el mensaje de error correspondiente.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

                # Se inicializa el contexto.
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                # Se actualiza el contexto.
                request, context = self.contextTotal(request, controlId, context)

                # Renderiza el template en base del contexto.
                return render(request, self.template_name, context=context)

        # Si se ha presionado el botón de 'Seleccionar Evidencia'.
        elif seleccionarEvidenciaButton == 'btn5':
            # Si se ha seleccionado algún control.
            if request.session["controlSelect"] != 'noSel':

                # Se guarda desde la sessión actual la información del selector de evidencias.
                selectorEvidencia = request.POST.get('selectorEvidencia')

                # Si hay algúna evidencia seleccionada.
                if selectorEvidencia != 'noSel':
                    # Obtiene las instancias de 'Assessmentguardados' y 'AssessmentCreados'.
                    assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                    control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                            control_id=request.session["controlSelect"])

                    # Verifica si el idioma del assessment está en inglés.
                    if assGuardado.idioma == 'en':
                        # Obtiene una instancia de 'Evidencerequestcatalog'.
                        evidencia = Evidencerequestcatalog.objects.get(evidence_request_references=selectorEvidencia)
                        # Obtiene una instancia de 'AsociacionEvidenciasGenericas'.
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia=evidencia, assessment=control)
                        # Se guarda en la bd.
                        eviGenerica.save()

                    # Si el idioma del assessment está en español.
                    else:
                        # Obtiene una instancia de 'Evidencerequestcatalog'.
                        evidencia = EvidencerequestcatalogEs.objects.get(evidence_request_references=selectorEvidencia)
                        # Obtiene una instancia de 'AsociacionEvidenciasGenericas'.
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia_id_es=evidencia, assessment=control)
                        # Se guarda en la bd.
                        eviGenerica.save()

                # Si no hay ninguna evidencia seleccionada.
                else:
                    # Inicializa el contexto.
                    context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                    # Actualiza el contexto.
                    request, context = self.contextTotal(request, request.session["controlSelect"], context)

                    # Se genera el mensaje de error correspondiente.
                    messages.error(request,
                                   'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')

                    # Renderiza el template en base del contexto.
                    return render(request, self.template_name, context=context)

            # Si no se ha seleccionado ningún control.
            else:
                # Se genera el mensaje de error correspondiente.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

                # Se inicializa el contexto.
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                # Se actualiza el contexto.
                request, context = self.contextTotal(request, request.session["controlSelect"], context)

                # Se renderiza el contexto en base del contexto.
                return render(request, self.template_name, context=context)

        # Si se ha presionado el botón de 'eliminar' en el cuadro de 'Evidencia'.
        elif btnEliminarEvidencia != '':
            # Obtiene una instancia de 'AsociacionEvidenciasGenericas' con el ID igual a 'btnEliminarEvidencia'.
            evidencia = AsociacionEvidenciasGenericas.objects.get(id=btnEliminarEvidencia)
            # Se elimina la evidencia.
            evidencia.delete()

            # Se inicializa el contexto.
            context = super(encuestaEntrevista, self).get_context_data(**knwargs)
            # Se actualiza el contexto.
            request, context = self.contextTotal(request, request.session["controlSelect"], context)

            # Se renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)
