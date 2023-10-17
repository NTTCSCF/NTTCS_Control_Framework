from .__imports__ import *


class assessment(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'Assessment' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/assessment.html"
    # Se hace una conexión a la base de datos.
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    # TODO: Check 'request' var.
    def contextTotal(self, request, select, assSelect, context):
        ''' Esta función se ha creado con el propósito de evitar la duplicación de código en el proyecto.
            Actualiza el contexto común en todas las páginas.'''

        # Obtener el objeto 'Assessmentguardados' correspondiente a 'assSelect'.
        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

        # Agregar 'assSelect' y 'assGuardado' al contexto.
        context["NombreAss"] = assSelect
        context["assessment"] = assGuardado
        # Agregar el assessment creado correspondiente a 'assGuardado' al contexto.
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

        # Obtener el objeto 'AssessmentCreados' relacionado a 'assGuardado' y 'select'.
        control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=select)

        lista = []
        ''' Esta lista es creada con tal de recorrer las evidencias en el template, independientemente
        de que esten en ingles o español. '''

        # Comprobar el idioma de 'assGuardado' y configurar el contexto en consecuencia
        if assGuardado.idioma == 'en':
            # Consulta para el desplegable de la valoración de madurez.
            context["valMad"] = MaturirtyTable.objects.all()
            # Se guardan las evidencias.
            context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()

            # Se añaden a la lista las asociaciones de evidencias genéricas relacionadas a 'control'.
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia_id]
        else:
            # Consulta para el desplegable de la valoración de madurez.
            context["valMad"] = MaturirtyTableEs.objects.all()
            # Se guardan las evidencias.
            context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

            # Se añaden a la lista las asociaciones de evidencias genéricas relacionadas a 'control'.
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia_id_es]

        # Se guarda la lista en el contexto.
        context["listaEvidencias"] = lista

        request.session["controlSelect"] = select
        # Se guarda el objeto de la clase 'AssessmentCreados' en el contexto.
        context["control"] = control
        context["criteriovaloracioncontexto"] = ['CCMM L0 \n No realizado',
                                                 'CCMM L1 \n Realizado de manera informal',
                                                 'CCMM L2 \n Planificado y rastreado',
                                                 'CCMM L3 \n Bien definido',
                                                 'CCMM L4 \n Controlado Cuantitativamente',
                                                 'CCMM L5 \n Mejorando Continuamente']

        # Recordemos que el campo 'criteriovaloracion' esta formado por diversas columnas
        # separadas por [-33--33-], por eso mismo se usa la función split.
        context["criteriovaloracion"] = control.criteriovaloracion.split('[-33--33-]')

        # Obtener las evidencias genericas asociadas a 'control'.
        context["evidencias"] = AsociacionEvidenciasGenericas.objects.filter(assessment=control)
        # Obtener las evidencias genericas asociadas a 'id_assessment'.
        context["evidencias2"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment=control)
        # Obtener todos los tipos de iniciativas.
        context["tiposIniciativas"] = TiposIniciativas.objects.all()
        # Obtener todas las iniciativas.
        context["iniciativas"] = Iniciativas.objects.all()

        # Obtener las evidencias recomendadas para 'select'.
        evidenciasRecomendadas = Assessment.objects.get(id=select).evidence_request_references

        # Comprobar si hay evidencias recomendadas.
        if evidenciasRecomendadas == '' or evidenciasRecomendadas is None:
            # Si no hay evidencias recomendadas, establecer 'recomendacion' como False.
            context["recomendacion"] = False
        else:
            # Si hay evidencias recomendadas, procesarlas.
            evidenciasRecomendadas = evidenciasRecomendadas.split('\n')
            # Variable usada para guardar las recomendaciones de cada control.
            r = ''

            for i in evidenciasRecomendadas:
                if assGuardado.idioma == 'en':
                    # Obtener la evidencia correspondiente en inglés.
                    evidencia = Evidencerequestcatalog.objects.get(evidence_request_references=i)
                    # Comprobar si la evidencia no está asociada a 'control'.
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia=evidencia, assessment=control):
                        # Añadir la evidencia a la recomendación.
                        r += i + ', '
                else:
                    # Obtener la evidencia correspondiente en español.
                    evidencia = EvidencerequestcatalogEs.objects.get(evidence_request_references=i)
                    # Comprobar si la evidencia no está asociada a 'control'
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia_id_es=evidencia, assessment=control):
                        # Añadir la evidencia a la recomendación.
                        r += i + ', '

            if r != '':
                # Si se encontraron evidencias recomendadas no asociadas, establecer 'recomendacion' como True.
                context["recomendacion"] = True
                # Almacenar las evidencias recomendadas no asociadas en 'eviRecomendada'.
                context["eviRecomendada"] = r[:len(r) - 2]
            else:
                # Si se encontraron evidencias recomendadas no asociadas, establecer 'recomendacion' como False.
                context["recomendacion"] = False

        # Devolver 'request' y el contexto.
        return request, context

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Guardamos el id (nombre) del assesment en una variable.
        assSelect = self.request.session.get('assessmentGuardado')
        # Se consigue de la bd el assessment correspondiente al id conseguido previamente.
        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
        # Actualizamos la fecha de la última modificación del assessment en formato YYYY/MM/DD.
        assGuardado.fecha_ultima_modificacion = datetime.now().isoformat().split('T')[0]
        # Se guardan los cambios en la bd.
        assGuardado.save()

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(assessment, self).get_context_data(**knwargs)
        # Se guarda en el contexto el nombre del assessment (o la id).
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

        # Actualizaremos el contexto en base del idioma.
        if assGuardado.idioma == 'en':
            # Consulta para el desplegable de la valoración de madurez.
            context["valMad"] = MaturirtyTable.objects.all()
            # Se guardan las evidencias.
            context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
        else:
            # Consulta para el desplegable de la valoración de madurez.
            context["valMad"] = MaturirtyTableEs.objects.all()
            # Se guardan las evidencias.
            context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

        # Se guardan los tipos de inicitaivas.
        context["tiposIniciativas"] = TiposIniciativas.objects.all()
        # Se guardan las inicitaivas existentes.
        context["iniciativas"] = Iniciativas.objects.all()

        self.request.session["controlSelect"] = 'noSel'

        # Se devuelve el contexto.
        return context

    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario. '''

        assSelect = request.session.get('assessmentGuardado')
        ''' Guardamos el id (nombre) del assesment en una variable. '''

        select = request.POST.get('selector')
        '''Valor de el selector de control.'''

        guardarValoracionBttn = request.POST.get('boton2')
        '''Valor del 'boton 2', que corresponde al botón de 'guardar valoración'.'''

        añadirEvidenciaBttn = request.POST.get('boton4')
        '''Valor del 'boton 4', que corresponde al botón de 'añadir evidencia'.'''

        seleccionarEvidenciaBttn = request.POST.get('boton5')
        '''Valor del 'boton 5', que corresponde al botón de 'seleccionar evidencia'.'''

        crearEvidenciaBttn = request.POST.get('boton6')
        '''Valor del 'boton 6', que corresponde al botón de 'crear iniciativa'.'''

        asignarIniciativaBttn = request.POST.get('boton7')
        '''Valor del 'boton 7', que corresponde al botón de 'asignar iniciativa'.'''

        boton8 = request.POST.get('boton8')
        '''Valor del 'boton 8', que corresponde al botón de 'añadir' cuando se recomiendan evidencias.'''

        btnEliminarEvidencia = request.POST.get('btnEliminarEvidencia')
        '''Valor del 'btnEliminarEvidencia'.'''

        # Se determina si se ha seleccionado el selector de marcos.
        if 'selector' in request.POST:
            # Si no se ha seleccionado ningún marco.
            if select == 'noSel':
                # Se coge el assessment guardado con el id del assessment seleccionado.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                context = super(assessment, self).get_context_data(**knwargs)
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

                # Actualizaremos el contexto en base del idioma.
                if assGuardado.idioma == 'en':
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTable.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                else:
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTableEs.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

                # Se guarda en una sessón del servidor el control seleccionado.
                request.session["controlSelect"] = select

                # Se guardan los tipos de inicitaivas.
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                # Se guardan las inicitaivas existentes.
                context["iniciativas"] = Iniciativas.objects.all()

                # Se renderiza el template a base del contexto.
                return render(request, self.template_name, context=context)

            else:
                # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                context = super(assessment, self).get_context_data(**knwargs)
                request, context = self.contextTotal(request, select, assSelect, context)

                # Se renderiza el template a base del contexto.
                return render(request, self.template_name, context=context)

        # Comprobamos si se ha pulsado el botón de 'guardar valoración'.
        elif guardarValoracionBttn == 'btn2':

            # Si se ha seleccionado ningún control.
            if request.session["controlSelect"] != 'noSel':
                # Conseguimos el assessment de la bd que se ha seleccionado anteriormente.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                ''' Se consigue el assessment de la base de datos y se actualiza con la información
                corresponiente del formulario. '''
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                control.respuesta = str(request.POST.get('respuesta'))
                control.valoracion = request.POST.get('valmad')
                control.valoracionobjetivo = request.POST.get('valmadob')
                control.save()

            # Si no se ha seleccionado ningún control.
            else:
                # Se crea un mensaje de error.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

            # Esto inicializa un diccionario llamado context con algunos datos de contexto.
            context = super(assessment, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session.get('controlSelect'), assSelect, context)

            # Se renderiza el template a base del contexto.
            return render(request, self.template_name, context=context)

        # Comprobamos si se ha pulsado el botón de 'guardar valoración'.
        elif añadirEvidenciaBttn == 'btn4':

            '''Tarjeta de Nueva Evidencia  '''
            # Se coge el input 'id referencia' de la nueva evidencia y se le concatena '-C', pues así
            # está guardada en la bd.
            idEvidencia = request.POST.get('idEvidencia') + '-C'
            # Valor del DescripcionEvidencia.
            descripcionEvidencia = request.POST.get('DescripcionEvidencia')
            # Valor del linkEvidencia.
            linkEvidencia = request.POST.get('linkEvidencia')

            # Se guarda el control seleccionado anteriormente.
            controlId = request.session["controlSelect"]

            # Si se ha seleccionado algún control.
            if controlId != 'noSel':
                # Si ni la id como la descripción de la evidencia están vacías.
                if idEvidencia != '' and descripcionEvidencia != '':
                    # Si la evidencia no existe en la base de datos, se puede crear.
                    if not Evidencias.objects.filter(evidencia_id=idEvidencia).exists():
                        # Se crea una nueva evidencia y se guarda en la BD.
                        ev = Evidencias(evidencia_id=idEvidencia, comentario=descripcionEvidencia, links=linkEvidencia,
                                        control_id=controlId,
                                        assessment=Assessmentguardados.objects.get(id_assessment=assSelect))
                        ev.save()

                        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                        # Obtenemos el assesment creado a partir de la información obtenida.
                        control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                control_id=request.session["controlSelect"])
                        # Se guarda el input de 'respuesta'.
                        control.respuesta = str(request.POST.get('respuesta'))
                        # Se guarda el input de 'valoración de madurez'.
                        control.valoracion = request.POST.get('valmad')
                        # Se guarda el input de 'valoración de madurez objetivo'.
                        control.valoracionobjetivo = request.POST.get('valmadob')
                        # Se guarda en la base de datos.
                        control.save()

                        # Se asocia la evidencia con el assessment creado.
                        evidencia = AsociacionEvidenciasCreadas(id_evidencia=ev, id_assessment=control)
                        # Se guarda en la BD.
                        evidencia.save()

                        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, assSelect, context)

                        # Renderiza el template en base el contexto.
                        return render(request, self.template_name, context=context)
                    # Si la evidencia  existe en la base de datos, nos se puede crear.
                    else:
                        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, controlId, assSelect, context)
                        # Se crea mensaje de error.
                        messages.error(request, 'EVIDENCIA INCORRECTA: La evidencia introducida ya existe')

                        # Renderiza el template en base el contexto.
                        return render(request, self.template_name, context=context)
                # Si la id o la descripción de la evidencia están vacías.
                else:
                    # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, controlId, assSelect, context)
                    # Se crea mensaje de error.
                    messages.error(request, 'EVIDENCIA INCORRECTA Necesita introducir un id y una descripcion para la '
                                            'evidencia')

                    # Renderiza el template en base el contexto.
                    return render(request, self.template_name, context=context)
            # Si no se ha seleccionado ningñun control.
            else:
                # Se crea un mensaje de error.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

                # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                context = super(assessment, self).get_context_data(**knwargs)
                # Se guarda el assessment de la tabla 'Assessmentguardados' en base del id del assessment seleccionado.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                # Guardamos en el contexto el identificador del assessment que, a su vez, es el nombre.
                context["NombreAss"] = assSelect
                # Se guarda en el contexto el assessment creado en base de la variable anterior.
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

                # Actualizaremos el contexto en base del idioma.
                if assGuardado.idioma == 'en':
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTable.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                else:
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTableEs.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

                # Se guardan los tipos de inicitaivas.
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                # Se guardan las inicitaivas existentes
                context["iniciativas"] = Iniciativas.objects.all()

                # Se renderizará el template en base del contexto.
                return render(request, self.template_name, context=context)

        # Detecta si se ha presionado el botón de 'seleccionar evidencia'.
        elif seleccionarEvidenciaBttn == 'btn5':

            # Si se ha seleccionado algún control.
            if request.session["controlSelect"] != 'noSel':
                # Se reoge el valor del selector de evidencia generica.
                selectorEvidencia = request.POST.get('selectorEvidencia')

                # Si se ha seleccionado alguna evidencia.
                if selectorEvidencia != 'noSel':
                    # Se elige el assessment guardado en base del nombre del assessment.
                    assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                    #
                    control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                            control_id=request.session["controlSelect"])
                    # Si el idioma del assessment esta en ingles.
                    if assGuardado.idioma == 'en':
                        '''Se actualiza la tabla de 'AsociacionEvidenciasGenericas'. '''
                        evidencia = Evidencerequestcatalog.objects.get(evidence_request_references=selectorEvidencia)
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia=evidencia, assessment=control)
                        eviGenerica.save()
                    else:
                        '''Se actualiza la tabla de 'AsociacionEvidenciasGenericas'. '''
                        evidencia = EvidencerequestcatalogEs.objects.get(evidence_request_references=selectorEvidencia)
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia_id_es=evidencia, assessment=control)
                        eviGenerica.save()

                    # Se elige el assessment guardado en base del nombre del assessment.
                    assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                    control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                            control_id=request.session["controlSelect"])
                    # Se guarda el input de 'respuesta'.
                    control.respuesta = str(request.POST.get('respuesta'))
                    # Se guarda el input de 'valoración de madurez'.
                    control.valoracion = request.POST.get('valmad')
                    # Se guarda el input de 'valoración de madurez objetivo'.
                    control.valoracionobjetivo = request.POST.get('valmadob')
                    # Se guarda en la bd.
                    control.save()
                    # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)

                    # Se renderiza la página en base del contexto.
                    return render(request, self.template_name, context=context)

                # Si no se ha seleccionado ninguna evidencia.
                else:
                    # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)

                    # Se crea un mensaje de error.
                    messages.error(request, 'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')

                    # Se renderiza la pagina en base del contexto.
                    return render(request, self.template_name, context=context)

            # Si no se ha sleccionado ningún control.
            else:
                # Se crea un mensaje de error
                messages.error(request, 'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')
                # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                context = super(assessment, self).get_context_data(**knwargs)
                # Se elige el assessment guardado en base del nombre del assessment.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                # Guardamos en el contexto el identificador del assessment que, a su vez, es el nombre.
                context["NombreAss"] = assSelect
                # Se guarda en el contexto el assessment creado en base de la variable anterior.
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

                # Actualizamos el contexto en función del idioma del assessment.
                if assGuardado.idioma == 'en':
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTable.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                else:
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTableEs.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

                # Se guardan los tipos de inicitaivas.
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                # Se guardan las inicitaivas existentes.
                context["iniciativas"] = Iniciativas.objects.all()

                # Se renderiza el template en función del contexto.
                return render(request, self.template_name, context=context)

        # Se comrpueba si se le ha dado al botón 'crear iniciativa'.
        elif crearEvidenciaBttn == 'btn6':

            selectorEvidencia = request.POST.get('selectorEvidenciaIniciativa')
            ''' Se recoge el valor del desplegable 'seleccione la evidencia'. '''

            nombreIniciativa = request.POST.get('nombreIniciativa')
            ''' Se recoge el valor del input 'nombre de la iniciativa'. '''

            DescripcionIniciativa = request.POST.get('DescripcionIniciativa')
            ''' Se recoge el valor del input 'descripción de la inciativa'. '''

            SelectorIniciativa = request.POST.get('SelectorIniciativa')
            ''' Se recoge el valor del desplegable 'seleccione el tipo de iniciativa. '''

            # Si se ha seleccionado un control.
            if request.session["controlSelect"] != 'noSel':
                # Si se ha seleccionado una evidencia.
                if selectorEvidencia != 'noSel':
                    # Si la iniciativa no existe, se crea en la bd.
                    if not Iniciativas.objects.filter(nombre=nombreIniciativa).exists():
                        # Si la evidencia introducida existe en la tabla 'Evidencerequestcatalog'.
                        if Evidencerequestcatalog.objects.filter(
                                evidence_request_references=selectorEvidencia).exists():

                            # Conseguimos el assessment de la tabla 'AssessmentCreados' en base del id del nombre del assessment.
                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])

                            '''Dependiendo del idioma del assessment guardamos la evidencia en un idioma u otro.'''
                            if assGuardado.idioma == 'en':
                                evidencia = Evidencerequestcatalog.objects.get(
                                    evidence_request_references=selectorEvidencia)
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia=evidencia,
                                                                                       assessment=control)
                            else:
                                evidencia = EvidencerequestcatalogEs.objects.get(
                                    evidence_request_references=selectorEvidencia)
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia_id_es=evidencia,
                                                                                       assessment=control)

                            # Se coge el tipo de la iniciativa en base del introducido en el desplegable.
                            tipoIniciativa = TiposIniciativas.objects.get(tipo=SelectorIniciativa)
                            # Añadimos la relación entre la tabla 'iniciativa' y 'tipos_iniciativas'.
                            iniciativa = Iniciativas(nombre=nombreIniciativa, descripcion=DescripcionIniciativa,
                                                     tipo=tipoIniciativa)
                            # Guardamos la inciativa en la BD.
                            iniciativa.save()

                            # Asociamos la tabla 'AsociacionEvidenciasGenericas' con la tabla 'iniciativa'.
                            asociacion.iniciativa = iniciativa
                            asociacion.save()

                            # Actualizamos la tabla 'assessment_creados' por los datos introducidos.
                            control.respuesta = str(request.POST.get('respuesta'))
                            control.valoracion = request.POST.get('valmad')
                            control.valoracionobjetivo = request.POST.get('valmadob')
                            control.save()

                            # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)

                            # Se renderiza el template en base del contexto.
                            return render(request, self.template_name, context=context)
                        # Si la evidencia no existe en la tabla 'Evidencerequestcatalog'.
                        else:
                            # Se consigue le evidencia de la base de datos.
                            evidencia = Evidencias.objects.get(evidencia_id=selectorEvidencia)

                            # Se relaciona el elemento de la tabla 'Assessmentguardados' con el de la tabla 'AssessmentCreados'
                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])
                            # Se asocia la evidencia con el control en la bd.
                            asociacion = AsociacionEvidenciasCreadas.objects.get(id_evidencia=evidencia,
                                                                                 id_assessment=control)
                            # Se relaciona la tabla 'tipoIniciativa' con 'Iniciativas' y se guarda en la BD.
                            tipoIniciativa = TiposIniciativas.objects.get(tipo=SelectorIniciativa)
                            iniciativa = Iniciativas(nombre=nombreIniciativa, descripcion=DescripcionIniciativa,
                                                     tipo=tipoIniciativa)
                            iniciativa.save()

                            # Se asocia el assessment con la iniciativa y se guarda en la BD.
                            asociacion.iniciativa = iniciativa
                            asociacion.save()

                            # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)

                            # Se renderiza el template en base del contexto.
                            return render(request, self.template_name, context=context)

                    # Si la iniciativa existe, salta un error.
                    else:
                        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                             context)
                        # Mensaje de error.
                        messages.error(request,
                                       'INICIATIVA INCORRECTA: El nombre introducido ya esta en uso')

                        # Se renderiza el template en base del contexto.
                        return render(request, self.template_name, context=context)
                # Si no se ha seleccionado una evidencia.
                else:
                    # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)
                    # Mensaje de error.
                    messages.error(request,
                                   'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')

                    # Se renderiza el template en base del contexto.
                    return render(request, self.template_name, context=context)

            # Si no se ha seleccionado ningún control.
            else:
                # Mensaje de error.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')

                # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                context = super(assessment, self).get_context_data(**knwargs)
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                # Guardamos en el contexto el identificador del assessment que, a su vez, es el nombre.
                context["NombreAss"] = assSelect
                # Se guarda en el contexto el assessment creado en base de la variable anterior.
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

                # Actualizamos el contexto en función del idioma del assessment.
                if assGuardado.idioma == 'en':
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTable.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                else:
                    # Consulta para el desplegable de la valoración de madurez.
                    context["valMad"] = MaturirtyTableEs.objects.all()
                    # Se guardan las evidencias.
                    context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

                # Se guardan los tipos de inicitaivas.
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                # Se guardan las inicitaivas existentes.
                context["iniciativas"] = Iniciativas.objects.all()

                # Se renderiza el template en base del contexto.
                return render(request, self.template_name, context=context)
        # Si se da al botón de 'Asignar Iniciativa'.
        elif asignarIniciativaBttn == 'btn7':

            selectEviasig = request.POST.get('selectEviasig')
            ''' Selector de evidencia. '''

            selectIniAsig = request.POST.get('selectIniAsig')
            ''' Selector de iniciativa. '''

            # Se comprueba si hay algún control seleccionado.
            if request.session["controlSelect"] != 'noSel':
                # Si se ha seleciconado alguna evidencia.
                if selectEviasig != 'noSel':
                    # Si se ha seleccionado alguna iniciativa.
                    if selectIniAsig != 'noSel':
                        # Si existe la evidencia en la bd.
                        if Evidencerequestcatalog.objects.filter(
                                evidence_request_references=selectEviasig).exists():

                            # Obtener el objeto 'Assessmentguardados' relacionado a 'assSelect'.
                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            # Obtener el objeto 'AssessmentCreados' relacionado a 'assGuardado' y 'controlSelect'.
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])
                            if assGuardado.idioma == 'en':
                                # Si el idioma es inglés, obtener la evidencia correspondiente en inglés.
                                evidencia = Evidencerequestcatalog.objects.get(
                                    evidence_request_references=selectEviasig)
                                # Obtener el objeto 'AsociacionEvidenciasGenericas' que cumpla las condiciones.
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia=evidencia,
                                                                                       assessment=control)
                            else:
                                # Si el idioma es español, obtener la evidencia correspondiente en español.
                                evidencia = EvidencerequestcatalogEs.objects.get(
                                    evidence_request_references=selectEviasig)
                                # Obtener el objeto 'AsociacionEvidenciasGenericas' que cumpla las condiciones.
                                asociacion = AsociacionEvidenciasGenericas.objects.get(evidencia_id_es=evidencia,
                                                                                       assessment=control)
                            # Asociar la iniciativa seleccionada a 'asociacion' y guardarla en la bd.
                            iniciativa = Iniciativas.objects.get(nombre=selectIniAsig)
                            asociacion.iniciativa = iniciativa
                            asociacion.save()
                            # Actualizar los campos de 'control' con los datos del formulario y guardalo en la bd.
                            control.respuesta = str(request.POST.get('respuesta'))
                            control.valoracion = request.POST.get('valmad')
                            control.valoracionobjetivo = request.POST.get('valmadob')
                            control.save()

                            # Actualizar el contexto.
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)
                            # Renderizar el template en base del contexto.
                            return render(request, self.template_name, context=context)

                        # Si no existe la evidencia en la bd.
                        else:
                            # Obtener la evidencia correspondiente a 'selectEviasig' desde la tabla 'Evidencias'.
                            evidencia = Evidencias.objects.get(evidencia_id=selectEviasig)
                            # Obtener el objeto 'Assessmentguardados' relacionado a 'assSelect'.
                            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)
                            # Obtener el objeto 'AssessmentCreados' relacionado a 'assGuardado' y 'controlSelect'.
                            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                                    control_id=request.session["controlSelect"])
                            # Obtener la asociación de evidencias creadas correspondiente a 'evidencia' y 'control'
                            asociacion = AsociacionEvidenciasCreadas.objects.get(id_evidencia=evidencia,
                                                                                 id_assessment=control)
                            # Asociar la iniciativa seleccionada a 'asociacion'
                            iniciativa = Iniciativas.objects.get(nombre=selectIniAsig)
                            asociacion.iniciativa = iniciativa
                            asociacion.save()

                            # Actualizar el contexto.
                            context = super(assessment, self).get_context_data(**knwargs)
                            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                                 context)
                            # Renderizar el template en base del contexto.
                            return render(request, self.template_name, context=context)
                    # Si no se ha seleccionado ninguna iniciativa.
                    else:
                        # Actualizar el contexto.
                        context = super(assessment, self).get_context_data(**knwargs)
                        request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                             context)
                        # Se crea un mensaje de error.
                        messages.error(request,
                                       'INICIATIVA INCORRECTA: Necesita seleccionar una iniciativa')

                        # Renderizar el template en base del contexto.
                        return render(request, self.template_name, context=context)
                # Si no se ha seleciconado ninguna evidencia.
                else:
                    # Actualizar el contexto.
                    context = super(assessment, self).get_context_data(**knwargs)
                    request, context = self.contextTotal(request, request.session["controlSelect"], assSelect,
                                                         context)
                    # Se crea un mensaje de error.
                    messages.error(request,
                                   'EVIDENCIA INCORRECTA: Necesita seleccionar una evidencia')

                    # Renderizar el template en base del contexto.
                    return render(request, self.template_name, context=context)
            # Si no hay ningñun control seleccionado.
            else:
                # Se crea un mensaje de error.
                messages.error(request,
                               'CONTROL INCORRECTO: Necesita seleccionar un control para realizar esta acción')  # Se crea mensage de error
                context = super(assessment, self).get_context_data(**knwargs)

                # Obtener el objeto 'Assessmentguardados' relacionado a 'assSelect'.
                assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

                # Agregar 'assSelect' y los objetos 'AssessmentCreados' relacionados a 'assGuardado' al contexto.
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

                # Comprobar el idioma de 'assGuardado' y configurar el contexto en consecuencia.
                if assGuardado.idioma == 'en':
                    # Se guarda la valoración de madurez en inglés.
                    context["valMad"] = MaturirtyTable.objects.all()
                    # Se guardan las evidencias genéricas en inglés.
                    context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
                else:
                    # Se guarda la valoración de madurez en español.
                    context["valMad"] = MaturirtyTableEs.objects.all()
                    # Se guardan las evidencias genéricas en español.
                    context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()

                # Agregar los tipos de iniciativas y todas las iniciativas al contexto.
                context["tiposIniciativas"] = TiposIniciativas.objects.all()
                context["iniciativas"] = Iniciativas.objects.all()

                # Renderizar el template a base del contexto.
                return render(request, self.template_name, context=context)
        # Si se ha dado al botón de añadir cuando se recomiendan evidencias.
        elif boton8 == 'btn8':
            # Obtener las evidencias recomendadas para el control seleccionado y dividirlas en una lista.
            evidenciasRecomendadas = Assessment.objects.get(
                id=request.session["controlSelect"]).evidence_request_references.split('\n')
            # Obtener el objeto 'Assessmentguardados' relacionado a 'assSelect'.
            assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

            # Iterar sobre las evidencias recomendadas.
            for i in evidenciasRecomendadas:
                # Obtener el objeto 'AssessmentCreados' relacionado a 'assGuardado' y 'controlSelect'.
                control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                        control_id=request.session["controlSelect"])
                if assGuardado.idioma == 'en':
                    # Si el idioma es inglés, obtener la evidencia correspondiente en inglés.
                    evidencia = Evidencerequestcatalog.objects.get(
                        evidence_request_references=i)
                    # Comprobar si no existe una asociación de evidencias genéricas entre 'evidencia' y 'control'.
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia=evidencia, assessment=control):
                        # Crear una nueva asociación de evidencias genéricas.
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia=evidencia, assessment=control)
                        eviGenerica.save()
                else:
                    # Si el idioma es inglés, obtener la evidencia correspondiente en español.
                    evidencia = EvidencerequestcatalogEs.objects.get(
                        evidence_request_references=i)
                    # Comprobar si no existe una asociación de evidencias genéricas entre 'evidencia' y 'control'.
                    if not AsociacionEvidenciasGenericas.objects.filter(evidencia_id_es=evidencia, assessment=control):
                        # Crear una nueva asociación de evidencias genéricas
                        eviGenerica = AsociacionEvidenciasGenericas(evidencia_id_es=evidencia, assessment=control)
                        eviGenerica.save()
            # Obtener de nuevo el objeto 'AssessmentCreados' relacionado a 'assGuardado' y 'controlSelect'.
            control = AssessmentCreados.objects.get(assessment=assGuardado,
                                                    control_id=request.session["controlSelect"])

            # Actualizar los campos de 'control' con los datos del formulario.
            control.respuesta = str(request.POST.get('respuesta'))
            control.valoracion = request.POST.get('valmad')
            control.valoracionobjetivo = request.POST.get('valmadob')
            control.save()

            # Actualizar el contexto.
            context = super(assessment, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)

            # Rendreizar el template a base del contexto.
            return render(request, self.template_name, context=context)

        # Comprovar si se ha apretado el botón de eliminar evidencia.
        elif btnEliminarEvidencia != '':
            # Se busca la evidencia que se quiere eliminar.
            evidencia = AsociacionEvidenciasGenericas.objects.get(id=btnEliminarEvidencia)
            # Se elimina de la bd.
            evidencia.delete()

            # Se actualiza el contexto.
            context = super(assessment, self).get_context_data(**knwargs)
            request, context = self.contextTotal(request, request.session["controlSelect"], assSelect, context)

            # Rendreizar el template a base del contexto.
            return render(request, self.template_name, context=context)
