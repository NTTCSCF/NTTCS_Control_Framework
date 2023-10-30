from .__imports__ import *


class planProyecto(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'planProyecto'. '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/planProyecto.html"

    def contexto(self, context):
        assSelect = self.request.session.get('assessmentGuardado')
        ass = Assessmentguardados.objects.get(id_assessment=assSelect)

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
        self.request.session["ProyectoSeleccionado"] = None
        context = super(planProyecto, self).get_context_data(**knwargs)
        context = self.contexto(context)
        return context

    def post(self, request, **knwargs):
        assSelect = request.session.get('assessmentGuardado')
        if 'crearProyecto' in request.POST:
            if request.POST.get('NombrePlan') != '' and request.POST.get('descripcionPlan') != '' and request.POST.get(
                    'riesgosPlan') != '' and request.POST.get('tipoPlan') != '' and request.POST.get(
                'duracionPlan') != '' and request.POST.get('costePlan') != '' and request.POST.get(
                'beneficioPlan') != '':
                ass = Assessmentguardados.objects.get(id_assessment=assSelect)
                if ass.plan_proyecto_mejora != None:
                    proyecto = ProyectosMejora(nombre=request.POST.get('NombrePlan'),
                                               descripcion=request.POST.get('descripcionPlan'),
                                               riesgos=request.POST.get('riesgosPlan'),
                                               tipo=request.POST.get('tipoPlan'),
                                               duracion=request.POST.get('duracionPlan'),
                                               capex=request.POST.get('capex'),
                                               opex=request.POST.get('opex'),
                                               beneficio=request.POST.get('beneficioPlan'),
                                               )
                    proyecto.save()
                    plan = ass.plan_proyecto_mejora
                    asociacion = AsociacionPlanProyectosProyectos(proyecto_mejora=proyecto, plan_proyecto=plan)
                    asociacion.save()

                    context = super(planProyecto, self).get_context_data(**knwargs)
                    context = self.contexto(context)

                    return render(request, self.template_name, context=context)
                else:
                    messages.error(request, 'ERROR, Necesitas crear un plan de proyecto antes de crear un proyecto')
            else:
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)
        elif 'editarProyecto' in request.POST:
            if request.POST.get('NombrePlan') != '' and request.POST.get('descripcionPlan') != '' and request.POST.get(
                    'riesgosPlan') != '' and request.POST.get('tipoPlan') != '' and request.POST.get(
                'duracionPlan') != '' and request.POST.get('capex') != '' and request.POST.get(
                'beneficioPlan') != '' and request.POST.get('opex') != '':
                ass = Assessmentguardados.objects.get(id_assessment=assSelect)
                proyecto = ProyectosMejora.objects.get(id=request.session["ProyectoEditar"])
                proyecto.nombre = request.POST.get('NombrePlan')
                proyecto.descripcion = request.POST.get('descripcionPlan')
                proyecto.riesgos = request.POST.get('riesgosPlan')
                proyecto.tipo = request.POST.get('tipoPlan')
                proyecto.duracion = request.POST.get('duracionPlan')
                proyecto.capex = request.POST.get('capex')
                proyecto.opex = request.POST.get('opex')
                proyecto.beneficio = request.POST.get('beneficioPlan')
                proyecto.save()

                context = super(planProyecto, self).get_context_data(**knwargs)
                context = self.contexto(context)

                return render(request, self.template_name, context=context)

            else:
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)
        elif 'NombrePlanProyecto' in request.POST:
            ass = Assessmentguardados.objects.get(id_assessment=assSelect)
            if ass.plan_proyecto_mejora == None:
                plan = PlanProyectoMejora(nombre=request.POST.get("NombrePlanProyecto"),
                                          descripcion=request.POST.get("descripcionPlanProyecto"))
                plan.save()
                ass = Assessmentguardados.objects.get(id_assessment=assSelect)
                ass.plan_proyecto_mejora = plan
                ass.save()
            else:
                plan = ass.plan_proyecto_mejora
                plan.nombre = request.POST.get("NombrePlanProyecto")
                plan.descripcion = request.POST.get("descripcionPlanProyecto")
                plan.save()
            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)
        elif 'btnSeleccionProyecto' in request.POST:
            request.session["ProyectoSeleccionado"] = request.POST.get('btnSeleccionProyecto')

            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)

        elif 'btnEditarProyecto' in request.POST:
            request.session["ProyectoEditar"] = request.POST.get('btnEditarProyecto')

            context = super(planProyecto, self).get_context_data(**knwargs)
            context["ProyectoEditar"] = ProyectosMejora.objects.get(id=request.session["ProyectoEditar"])
            context["duracion"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).duracion)
            context["capex"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).capex)
            context["opex"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).opex)
            context["beneficio"] = str(ProyectosMejora.objects.get(id=request.session["ProyectoEditar"]).beneficio)
            context["editandoProyecto"] = True
            context = self.contexto(context)
            return render(request, self.template_name, context=context)

        elif 'selectorIniciativasg' in request.POST:
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])
            iniciaticasSelect = request.POST.getlist('selectorIniciativasg')
            for i in iniciaticasSelect:
                if not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                         iniciativa=Iniciativas.objects.get(
                                                                             nombre=i)).exists():
                    asociacion = AsociacionProyectoMejoraIniciativa(proyecto=plan,
                                                                    iniciativa=Iniciativas.objects.get(nombre=i))
                    asociacion.save()
            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)

        elif 'selectorIniciativasc' in request.POST:
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])
            iniciaticasSelect = request.POST.getlist('selectorIniciativasc')

            for i in iniciaticasSelect:
                if not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan,
                                                                         iniciativa=Iniciativas.objects.get(
                                                                             nombre=i)).exists():
                    asociacion = AsociacionProyectoMejoraIniciativa(proyecto=plan,
                                                                    iniciativa=Iniciativas.objects.get(nombre=i))
                    asociacion.save()
            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)

        elif 'btnAnadirRecomendacion' in request.POST:
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])
            iniciaticasSelect = request.POST.get('btnAnadirRecomendacion')
            if not AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan, iniciativa=Iniciativas.objects.get(
                    nombre=iniciaticasSelect)).exists():
                asociacion = AsociacionProyectoMejoraIniciativa(proyecto=plan,
                                                                iniciativa=Iniciativas.objects.get(
                                                                    nombre=iniciaticasSelect))
                asociacion.save()
            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)

        elif 'btnEliminarAsociacion' in request.POST:
            plan = ProyectosMejora.objects.get(id=request.session["ProyectoSeleccionado"])
            iniciaticasSelect = request.POST.get('btnEliminarAsociacion')
            if AsociacionProyectoMejoraIniciativa.objects.filter(proyecto=plan, iniciativa=Iniciativas.objects.get(
                    nombre=iniciaticasSelect)).exists():
                asociacion = AsociacionProyectoMejoraIniciativa.objects.get(proyecto=plan,
                                                                            iniciativa=Iniciativas.objects.get(
                                                                                nombre=iniciaticasSelect))
                asociacion.delete()
            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)

        elif 'btnDepen' in request.POST:
            request.session["proyectoMejora"] = request.POST.get('btnDepen')
            request.session["assessmentGuardado"] = assSelect

            # Redirección hacia la url especificada en base del nombre.
            return redirect("dependencias")


            """activo = request.POST.getlist('activoDepen')
            proyecto = ProyectosMejora.objects.get(id=request.POST.get('proyecto').split(" - ")[0])
            if DependenciaProyecto.objects.filter(proyecto=proyecto).exists():
                depen = DependenciaProyecto.objects.filter(proyecto=proyecto)
                depen.delete()
            for i in activo:
                percentaje = request.POST.get('porcentajeDepen' + str(i))
                dependencia = DependenciaProyecto(proyecto=proyecto,
                                                  proyecto_asociado=ProyectosMejora.objects.get(id=i),
                                                  porcentaje=percentaje)
                dependencia.save()
            context = super(planProyecto, self).get_context_data(**knwargs)
            context = self.contexto(context)
            return render(request, self.template_name, context=context)"""
