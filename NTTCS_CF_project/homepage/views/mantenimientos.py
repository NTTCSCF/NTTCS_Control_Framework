from .__imports__ import *

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


# Clase para la pagina de MantenimientoEvidencias
class MantenimientoEvidenciasEs(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoEvidenciasEs.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:

            evidence_request_references = request.POST.get(
                'evidence_request_references')  # valor del input de evidence_request_references
            area_of_focus = request.POST.get('area_of_focus')  # valor del input de area_of_focus
            artifact = request.POST.get('artifact')  # valor del input de artifact
            artifact_description = request.POST.get('artifact_description')  # valor del input de artifact_description
            control_mappings = request.POST.get('control_mappings')  # valor del input de control_mappings
            if not EvidencerequestcatalogEs.objects.filter(
                    evidence_request_references=evidence_request_references).exists():
                if evidence_request_references != '' and area_of_focus != '' and artifact != '' and artifact_description != '' and control_mappings != '':
                    insert = EvidencerequestcatalogEs(evidence_request_references=evidence_request_references,
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
            consulta = EvidencerequestcatalogEs.objects.get(
                evidence_request_references=evidence_request_references)  # consulta para seleccionar el objeto que corresponde con la ultima busqueda
            consulta.area_of_focus = area_of_focus
            consulta.artifact = artifact
            consulta.artifact_description = artifact_description
            consulta.control_mappings = control_mappings
            consulta.save()  # fijamos los valores y los guardamos.
        elif 'eliminar' in request.POST:
            evidence_request_references = request.POST.get(
                'evidence_request_references')  # valor del input de evidence_request_references

            consulta = EvidencerequestcatalogEs.objects.get(evidence_request_references=evidence_request_references)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(EvidencerequestcatalogEs.objects.all(), 50)
        context = super(MantenimientoEvidenciasEs, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(EvidencerequestcatalogEs.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(EvidencerequestcatalogEs.objects.all(), 50)
        context = super(MantenimientoEvidenciasEs, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(EvidencerequestcatalogEs.objects.all())
        return context


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


class MantenimientoPreguntasEs(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/MantenimientoPreguntasEs.html"

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):

        if 'insertar' in request.POST:
            control_question = request.POST.get('control_question')  # valor del input de control_question
            control_description = request.POST.get('control_description')  # valor del input de control_description
            id = request.POST.get('id')  # valor del input de id
            if not AssessmentEs.objects.filter(id=id).exists():
                if control_question != '' and control_description != '' and id != '':
                    insert = AssessmentEs(id=id, control_question=control_question,
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
            consulta = AssessmentEs.objects.get(id=id)  # si esta en la tabla seleccionamos el ojeto en la tabla
            consulta.control_description = control_description
            consulta.control_question = control_question
            consulta.save()  # fijamos los valores y los guardamos..
        elif 'eliminar' in request.POST:
            id = request.POST.get('id')  # valor del input de id

            consulta = AssessmentEs.objects.get(id=id)
            consulta.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

        page = self.request.GET.get('page', 1)
        paginator = Paginator(AssessmentEs.objects.all(), 50)
        context = super(MantenimientoPreguntasEs, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(AssessmentEs.objects.all())
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.

    # funcion que envia el contexto de la pagina.
    def get_context_data(self, **knwargs):
        page = self.request.GET.get('page', 1)
        paginator = Paginator(AssessmentEs.objects.all(), 50)
        context = super(MantenimientoPreguntasEs, self).get_context_data(**knwargs)
        context["entity"] = paginator.page(page)
        context["paginator"] = paginator
        context["lenConsulta"] = len(AssessmentEs.objects.all())
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
                request.session['inicio'] = request.session['inicio'] - 100
        elif 'sig' in request.POST:
            if request.session['inicio'] < AsociacionMarcos.objects.all().count():
                request.session['inicio'] = request.session['inicio'] + 100
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
            c.delete()  # seleccionamos el objeto de la ultima busqueda y lo eliminamos.

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
                                          criteriovaloracion=criterio, valoracionobjetivo=valoracionobjetivo,
                                          respuesta=respuesta, valoracion=valoracion)
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
            assGuardado = Assessmentguardados.objects.get(id_assessment=self.request.session["seleccion"])
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