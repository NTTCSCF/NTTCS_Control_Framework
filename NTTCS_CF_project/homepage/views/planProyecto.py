from .__imports__ import *


class planProyecto(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'planProyecto'. '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/planProyecto.html"

    def contexto(self, context):
        '''Función auxiliar que se usa en la función 'get_context_data' para actualizar el contexto.'''

        # Obtención de 'assessmentGuardado' de la sesión.
        assSelect = self.request.session.get('assessmentGuardado')
        # Obtención de un objeto de Assessmentguardados basado en 'assSelect'.
        ass = Assessmentguardados.objects.get(id_assessment=assSelect)

        #
        if self.request.session["ProyectoSeleccionado"] != None:
            if ProyectosMejora.objects.filter(id=self.request.session["ProyectoSeleccionado"]).exists():
                plan = ProyectosMejora.objects.get(id=self.request.session["ProyectoSeleccionado"])

                g = []
                c = []
                for i in plan.descripcion.split(" "):
                    p = AsociacionEvidenciasGenericas.objects.filter(assessment__assessment=ass,
                                                                     iniciativa__descripcion__icontains=i)
                    for s in p:
                        if s not in g and not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                                                iniciativa=s.iniciativa).exists():
                            g += [s]
                    p = AsociacionEvidenciasCreadas.objects.filter(id_assessment__assessment=ass,
                                                                   iniciativa__descripcion__icontains=i)
                    for s in p:
                        if s not in c and not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                                                iniciativa=s.iniciativa).exists():
                            c += [s]
                context["recomendacion"] = g + c
                context["asociadas"] = AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan)
                asoci = []
                for i in AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan):
                    asoci += [i.iniciativa.id]
                context["idAsoci"] = asoci
            context["ProyectoSeleccionado"] = ProyectosMejora.objects.get(
                id=self.request.session["ProyectoSeleccionado"])
        else:
            context["ProyectoSeleccionado"] = self.request.session["ProyectoSeleccionado"]
        if ass.plan_proyecto_mejora != None:
            context["plan"] = ass.plan_proyecto_mejora
        context["proyectos"] = AsociacionPlanProyectosProyectos.objects.filter(plan_proyecto=ass.plan_proyecto_mejora)
        if AsociacionPlanProyectosProyectos.objects.filter(plan_proyecto=ass.plan_proyecto_mejora).exists():
            context["primero"] = \
                AsociacionPlanProyectosProyectos.objects.filter(plan_proyecto=ass.plan_proyecto_mejora)[
                    0].proyecto_mejora.id

        context["iniciativas"] = AsociacionEvidenciasGenericas.objects.filter(assessment__assessment=ass)
        context["iniciativasc"] = AsociacionEvidenciasCreadas.objects.filter(id_assessment__assessment=ass)
        context["assess"] = Assessmentguardados.objects.get(id_assessment=assSelect)
        context["dependencias"] = DependenciaProyecto.objects.all()


        return context

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Aquí se inicializa la variable de sesión "ProyectoSeleccionado" con el valor None.
        self.request.session["ProyectoSeleccionado"] = None

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(planProyecto, self).get_context_data(**knwargs)

        # Aquí se llama al método 'self.contexto' para modificar o ampliar el diccionario de contexto.
        context = self.contexto(context)

        # Devuelve el contexto.
        return context

    def post(self, request, **knwargs):
        '''Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        # Obtención de 'assessmentGuardado' de la sesión.
        assSelect = request.session.get('assessmentGuardado')

        # Se comprueba que se haya presionado el botón de crear proyecto.
        if 'crearProyecto' in request.POST:
            # Verificación de si todos los campos requeridos tienen valores válidos.
            if request.POST.get('NombrePlan') != ''\
                    and request.POST.get('descripcionPlan') != '' \
                    and request.POST.get('riesgosPlan') != '' \
                    and request.POST.get('tipoPlan') != '' \
                    and request.POST.get('duracionPlan') != '' \
                    and request.POST.get('costePlan') != '' \
                    and request.POST.get('beneficioPlan') != '':

                # Obtención de un objeto de Assessmentguardados basado en 'assSelect'.
                ass = Assessmentguardados.objects.get(id_assessment=assSelect)

                # Verificación de si existe un plan de proyecto de mejora.
                if ass.plan_proyecto_mejora != None:
                    # Creación y guardado de un objeto ProyectosMejora.
                    proyecto = ProyectosMejora(nombre=request.POST.get('NombrePlan'),
                                               descripcion=request.POST.get('descripcionPlan'),
                                               riesgos=request.POST.get('riesgosPlan'),
                                               tipo=request.POST.get('tipoPlan'),
                                               duracion=request.POST.get('duracionPlan'),
                                               capex=request.POST.get('capex'),
                                               opex=request.POST.get('opex'),
                                               beneficio=request.POST.get('beneficioPlan'))
                    proyecto.save()

                    # Obtención de 'plan_proyecto' y creación de una asociación.
                    plan = ass.plan_proyecto_mejora
                    asociacion = AsociacionPlanProyectosProyectos(proyecto_mejora=proyecto, plan_proyecto=plan)
                    asociacion.save()

                    # Esto inicializa un diccionario llamado context con algunos datos de contexto.
                    context = super(planProyecto, self).get_context_data(**knwargs)
                    # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
                    context = self.contexto(context)

                    # Renderiza el template en base del contexto.
                    return render(request, self.template_name, context=context)
                # TODO: Innecesario
                else:
                    # Se crea el mensaje de error.
                    messages.error(request, 'ERROR, Necesitas crear un plan de proyecto antes de crear un proyecto')
            else:
                # Se crea el mensaje de error.
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            # Esto inicializa un diccionario llamado context con algunos datos de contexto.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Comprovación si se da al botón de editar.
        elif 'editarProyecto' in request.POST:
            # Verificación de si todos los campos requeridos tienen valores válidos.
            if request.POST.get('NombrePlan') != '' \
                    and request.POST.get('descripcionPlan') != '' \
                    and request.POST.get('riesgosPlan') != '' \
                    and request.POST.get('tipoPlan') != '' \
                    and request.POST.get('duracionPlan') != '' \
                    and request.POST.get('capex') != '' \
                    and request.POST.get('beneficioPlan') != '' \
                    and request.POST.get('opex') != '':

                ass = Assessmentguardados.objects.get(id_assessment=assSelect)
                # Obtención de un objeto ProyectosMejora basado en el id de sesión "ProyectoEditar".
                proyecto = ProyectosMejora.objects.get(id=request.session["ProyectoEditar"])

                # Actualización de los campos del objeto ProyectosMejora con los valores del formulario.
                proyecto.nombre = request.POST.get('NombrePlan')
                proyecto.descripcion = request.POST.get('descripcionPlan')
                proyecto.riesgos = request.POST.get('riesgosPlan')
                proyecto.tipo = request.POST.get('tipoPlan')
                proyecto.duracion = request.POST.get('duracionPlan')
                proyecto.capex = request.POST.get('capex')
                proyecto.opex = request.POST.get('opex')
                proyecto.beneficio = request.POST.get('beneficioPlan')
                proyecto.save()

                # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
                context = super(planProyecto, self).get_context_data(**knwargs)
                # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
                context = self.contexto(context)

                # Renderiza el template an base al contexto.
                return render(request, self.template_name, context=context)

            # Si los campos están vacíos.
            else:
                # Se crea un mensaje de error.
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Se renderiza el template en base al contexto.
            return render(request, self.template_name, context=context)

        elif 'NombrePlanProyecto' in request.POST:
            # Obtención de un objeto Assessmentguardados basado en 'assSelect'.
            ass = Assessmentguardados.objects.get(id_assessment=assSelect)

            # Verificación de que no existe un plan de proyecto de mejora.
            if ass.plan_proyecto_mejora == None:

                # Creación de un nuevo objeto PlanProyectoMejora.
                plan = PlanProyectoMejora(nombre=request.POST.get("NombrePlanProyecto"),
                                          descripcion=request.POST.get("descripcionPlanProyecto"))
                # Se guarda el objeto en la BD.
                plan.save()

                # Se consigue la asesoría seleccionada.
                ass = Assessmentguardados.objects.get(id_assessment=assSelect)
                # Se actualiza la asesoría con el plan de proyecto.
                ass.plan_proyecto_mejora = plan
                # Se guarda el cambio en la BD.
                ass.save()

            # Si existe un poryecto de mejora.
            else:
                # Se consigue el plan de procto de mejora.
                plan = ass.plan_proyecto_mejora
                # Se actualiza el nombre.
                plan.nombre = request.POST.get("NombrePlanProyecto")
                # Se actualiza la descripción.
                plan.descripcion = request.POST.get("descripcionPlanProyecto")
                # Se actualiza en la BD.
                plan.save()

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderizar el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el botón de seleccionar en el carrusel del plan de proyecto.
        elif 'btnSeleccionProyecto' in request.POST:
            # Se guarda en el contexto el proyecto seleccionado.
            request.session["ProyectoSeleccionado"] = request.POST.get('btnSeleccionProyecto')

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderizar el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se presiona el botón de editar en el carrusel del plan de proyecto.
        elif 'btnEditarProyecto' in request.POST:
            # Se guarda en el contexto el proyecto seleccionado.
            request.session["ProyectoEditar"] = request.POST.get('btnEditarProyecto')

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)

            # Obtención de un objeto ProyectosMejora basado en el id de sesión "ProyectoEditar".
            context["ProyectoEditar"] = ProyectosMejora.objects.get(id=request.session["ProyectoEditar"])

            # Asignación de la duración, capex, opex y beneficio del proyecto del formulario al contexto.
            context["duracion"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).duracion)
            context["capex"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).capex)
            context["opex"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).opex)
            context["beneficio"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).beneficio)
            context["editandoProyecto"] = True

            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderizar el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se ha presionado en el selector de iniciativas genericas.
        elif 'selectorIniciativasg' in request.POST:
            # Obtención de un objeto ProyectosMejora basado en el proyecto seleccionado.
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])

            # Obtención de la lista de iniciativas genericas seleccionadas en el formulario.
            iniciaticasSelect = request.POST.getlist('selectorIniciativasg')

            # Bucle para crear asociaciones entre el proyecto y las iniciativas seleccionadas.
            for i in iniciaticasSelect:
                # Si la iniciativa no esta asociada con el proyecto.
                if not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                         iniciativa=Iniciativas.objects.get(nombre=i)).exists():
                    # Se asocia la iniciativa con el proyecto.
                    asociacion = AsociacionProyectoMejoraIniciativa(proyecto=plan,
                                                                    iniciativa=Iniciativas.objects.get(nombre=i))
                    # Se guarda en la BD.
                    asociacion.save()

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se ha presionado en el selector de iniciativas creativas.
        elif 'selectorIniciativasc' in request.POST:
            # Obtención de un objeto ProyectosMejora basado en el proyecto seleccionado.
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])

            # Obtención de la lista de iniciativas creadas seleccionadas en el formulario.
            iniciaticasSelect = request.POST.getlist('selectorIniciativasc')

            # Bucle para crear asociaciones entre el proyecto y las iniciativas seleccionadas.
            for i in iniciaticasSelect:
                # Si la iniciativa no esta asociada con el proyecto.
                if not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                         iniciativa=Iniciativas.objects.get(nombre=i)).exists():
                    # Se asocia la iniciativa con el proyecto.
                    asociacion = AsociacionProyectoMejoraIniciativa(proyecto=plan,
                                                                    iniciativa=Iniciativas.objects.get(nombre=i))
                    # Se guarda en la BD.
                    asociacion.save()

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se da al botoón de 'añadir' en la recomendación de iniciativas.
        elif 'btnAnadirRecomendacion' in request.POST:
            # Obtención de un objeto ProyectosMejora basado en el proyecto seleccionado.
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])

            # Se consigue la iniciativa recomendada.
            iniciaticasSelect = request.POST.get('btnAnadirRecomendacion')

            # Verificación de si no existe ya una asociación entre el proyecto y la iniciativa seleccionada.
            if not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                     iniciativa=Iniciativas.objects.get(nombre=iniciaticasSelect)).exists():

                # Se crea la asociación entre el proyecto y la iniciativa.
                asociacion = AsociacionProyectoMejoraIniciativa(proyecto=plan,
                                                                iniciativa=Iniciativas.objects.get(nombre=iniciaticasSelect))
                # Se guarda en la BD.
                asociacion.save()

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Botón de eliminar en 'Iniciativas Asociadas'.
        elif 'btnEliminarAsociacion' in request.POST:
            # Obtención de un objeto ProyectosMejora basado en el proyecto seleccionado.
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])

            # Se consigue la iniciativa recomendada.
            iniciaticasSelect = request.POST.get('btnEliminarAsociacion')

            # Verificación de si existe una asociación entre el proyecto y la iniciativa seleccionada.
            if AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                 iniciativa=Iniciativas.objects.get(nombre=iniciaticasSelect)).exists():
                # Se crea la asociación entre el proyecto y la iniciativa.
                asociacion = AsociacionProyectoMejoraIniciativa.objects.get(proyecto=plan,
                                                                            iniciativa=Iniciativas.objects.get(nombre=iniciaticasSelect))
                # Se elimina dicha asociación.
                asociacion.delete()

            # Obtención de 'context' y 'contexto' y renderizado de la plantilla.
            context = super(planProyecto, self).get_context_data(**knwargs)
            # Aquí se llama al método 'self.contexto' para modificar el diccionario de contexto.
            context = self.contexto(context)

            # Renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Si se da al botón de 'dependencias' en el carrusel.
        elif 'btnDepen' in request.POST:
            # Se actualiza la variable de sesión "proyectoMejora" con el valor de la dependencia.
            request.session["proyectoMejora"] = request.POST.get('btnDepen')
            # Se actualiza la variable de sesión "assessmentGuardado" con el valor de 'assSelect'.
            request.session["assessmentGuardado"] = assSelect

            # Redirección hacia la url especificada en base del nombre.
            return redirect("dependencias")

