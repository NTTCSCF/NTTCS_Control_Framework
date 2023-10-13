from .__imports__ import *

# Clase para la pagina de Entrevista
class encuestaEntrevista(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/EncuestaEntrevista.html"

    def contextTotal(self, request, select, context):

        entre = self.request.session.get('EntrevistaEditar')
        entrevista = Entrevistas.objects.get(id=entre)
        assSelect = entrevista.assesment.id_assessment
        assGuardado = entrevista.assesment
        e = entrevista.grupocontroles.split('\n')
        e = e[:len(e) - 1]

        context["primero"] = False
        context["ultimo"] = False
        if e.index(select) == len(e) - 1:
            context["ultimo"] = True
        elif e.index(select) == 0:
            context["primero"] = True

        context["controlEntrevista"] = e[:len(e)]
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=select)
        context["control"] = control
        self.request.session["controlSelect"] = select
        context["evidencias"] = AsociacionEvidenciasGenericas.objects.filter(assessment=control)
        context["evidencias2"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment=control)
        if assGuardado.idioma == 'en':
            context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
            lista = []
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia]
            context["listaEvidencias"] = lista
        else:
            context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()
            lista = []
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia_id_es]
            context["listaEvidencias"] = lista
        return request, context

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        entre = self.request.session.get('EntrevistaEditar')
        entrevista = Entrevistas.objects.get(id=entre)
        context = super(encuestaEntrevista, self).get_context_data(**knwargs)
        assSelect = entrevista.assesment.id_assessment
        assGuardado = entrevista.assesment
        e = entrevista.grupocontroles.split('\n')
        e = e[:len(e) - 1]
        context["controlEntrevista"] = e
        context["ultimo"] = False
        context["primero"] = True
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        control = AssessmentCreados.objects.get(assessment=assGuardado, control_id=e[0])
        if assGuardado.idioma == 'en':
            context["evidenciasGenerricas"] = Evidencerequestcatalog.objects.all()
            lista = []
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia]
            context["listaEvidencias"] = lista
        else:
            context["evidenciasGenerricas"] = EvidencerequestcatalogEs.objects.all()
            lista = []
            for i in AsociacionEvidenciasGenericas.objects.filter(assessment=control):
                lista += [i.evidencia_id_es]
            context["listaEvidencias"] = lista

        context["control"] = control
        self.request.session["controlSelect"] = e[0]
        context["evidencias"] = AsociacionEvidenciasGenericas.objects.filter(assessment=control)
        context["evidencias2"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment=control)
        return context

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):
        entre = request.session.get('EntrevistaEditar')
        entrevista = Entrevistas.objects.get(id=entre)
        assSelect = entrevista.assesment.id_assessment
        select = request.POST.get('selector')  # valor de el selector de control
        boton2 = request.POST.get('boton2')  # valor del boton 2
        boton3 = request.POST.get('boton3')  # valor del boton 3
        boton4 = request.POST.get('boton4')  # valor del boton 4
        boton5 = request.POST.get('boton5')  # valor del boton 5
        boton6 = request.POST.get('boton6')  # valor del boton 6
        boton7 = request.POST.get('boton7')  # valor del boton 7
        btnEliminarEvidencia = request.POST.get('btnEliminarEvidencia')  # valor del btnEliminarEvidencia

        if 'selector' in request.POST:  # se recoge la pulsacion del select
            if select == 'noSel':
                entrevista = Entrevistas.objects.get(id=entre)
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                assSelect = entrevista.assesment.id_assessment
                assGuardado = entrevista.assesment
                e = entrevista.grupocontroles.split('\n')
                context["controlEntrevista"] = e[:len(e) - 1]
                context["NombreAss"] = assSelect
                context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
                self.request.session["controlSelect"] = 'noSel'
                return render(request, self.template_name, context=context)
            else:
                context = super(encuestaEntrevista, self).get_context_data(**knwargs)
                request, context = self.contextTotal(request, select, context)
                return render(request, self.template_name, context=context)

        elif boton2 == 'btn2':  # recogemos la pulsacion del boton de guardar valoracion
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

        elif boton6 == 'btn6':  # recogemos la pulsacion del boton de guardar valoracion
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

        elif boton7 == 'btn7':  # recogemos la pulsacion del boton de guardar valoracion
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

        elif boton3 == 'btn3':  # recogemos la pulsacion del boton de guardar valoracion
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

        elif boton5 == 'btn5':  # if encargado de rellenar las evidencias
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
