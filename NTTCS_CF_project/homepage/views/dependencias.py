from .__imports__ import *


class dependencias(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'dependencias' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/dependencias.html"

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        '''Asegura que cualquier funcionalidad definida en las clases base 'LoginRequiredMixin' y 'TemplateView'
        se ejecute antes de personalizarla en la subclase ajustesAssesssment.'''

        # Guardamos el id (nombre) del assesment en una variable.
        assSelect = self.request.session.get('assessmentGuardado')
        # Guardamos el id del proeycto en una variable.
        proyect = self.request.session.get('proyectoMejora')
        # Se consigue de la bd el assessment correspondiente al id conseguido previamente.
        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

        proyecto = ProyectosMejora.objects.get(id=proyect)

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(dependencias, self).get_context_data(**knwargs)
        # Se guarda en el contexto el nombre del assessment (o la id).
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        context["depen"] = DependenciaProyecto.objects.filter(proyecto=proyecto)
        depen = DependenciaProyecto.objects.filter(proyecto=proyecto)
        context["proyec"] = proyecto
        proyectos = []
        proy = AsociacionPlanProyectosProyectos.objects.filter(plan_proyecto=assGuardado.plan_proyecto_mejora)
        for j in proy:
            esta = False
            if j.proyecto_mejora.id == proyecto.id:
                esta = True
            for i in depen:
                if i.proyecto_asociado.id == j.proyecto_mejora.id:
                    esta = True
                    break
            if not esta:
                proyectos += [j]

        context["proyectos"] = proyectos
        return context

    def post(self, request, **knwargs):
        '''Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''
        if 'btnDepen' in request.POST:

            activo = request.POST.getlist('activoDepen')
            proyecto = ProyectosMejora.objects.get(id=self.request.session.get('proyectoMejora'))
            if DependenciaProyecto.objects.filter(proyecto=proyecto).exists():
                depen = DependenciaProyecto.objects.filter(proyecto=proyecto)
                depen.delete()
            for i in activo:
                percentaje = request.POST.get('porcentajeDepen' + str(i))
                dependencia = DependenciaProyecto(proyecto=proyecto,
                                                  proyecto_asociado=ProyectosMejora.objects.get(id=i),
                                                  porcentaje=percentaje)
                dependencia.save()

        # Redirección hacia la url especificada en base del nombre.
        return redirect("planProyecto")
