from .__imports__ import *


class ajustesAssessment(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'ajustesAssesssment' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/ajustesAssessment.html"
    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        '''Asegura que cualquier funcionalidad definida en las clases base 'LoginRequiredMixin' y 'TemplateView'
        se ejecute antes de personalizarla en la subclase ajustesAssesssment.'''

        # Guardamos el id (nombre) del assesment en una variable.
        assSelect = self.request.session.get('assessmentGuardado')
        # Se consigue de la bd el assessment correspondiente al id conseguido previamente.
        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(ajustesAssessment, self).get_context_data(**knwargs)
        # Se guarda en el contexto el nombre del assessment (o la id).
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)

        return context

    def post(self, request, **knwargs):
        '''Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''
        if 'btnEliminar' in request.POST:
            control = AssessmentCreados.objects.get(id=request.POST.get('btnEliminar'))
            control.delete()

        # Guardamos el id (nombre) del assesment en una variable.
        assSelect = self.request.session.get('assessmentGuardado')
        # Se consigue de la bd el assessment correspondiente al id conseguido previamente.
        assGuardado = Assessmentguardados.objects.get(id_assessment=assSelect)

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(ajustesAssessment, self).get_context_data(**knwargs)
        # Se guarda en el contexto el nombre del assessment (o la id).
        context["NombreAss"] = assSelect
        context["assess"] = AssessmentCreados.objects.filter(assessment=assGuardado)
        return render(request, self.template_name, context=context)