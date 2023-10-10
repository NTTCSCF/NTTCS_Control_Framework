from .__imports__ import *

class entrevistasUsuarios(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/EntrevistasUsuario.html"

    def get_context_data(self, **knwargs):
        context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
        context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
        context["proyectoSelec"] = ''
        context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
        context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
        return context

    def post(self, request, **knwargs):
        if 'selectorProyecto' in request.POST:
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSelec"] = request.POST.get('selectorProyecto')
            context["proyectoSeleccionado"] = True
            request.session["proyectoSeleccionado"] = request.POST.get('selectorProyecto')
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.POST.get('selectorProyecto')), assessment__archivado=0)
            context["marcos"] = AsociacionMarcos.objects.all()
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context=context)

        elif 'selectorAssessment' in request.POST:
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSelec"] = request.session.get('proyectoSeleccionado')
            context["proyectoSeleccionado"] = True
            request.session["proyectoSeleccionado"] = request.session.get('proyectoSeleccionado')

            context["assessSelec"] = request.POST.get('selectorAssessment')
            context["assessmentSeleccionado"] = True
            request.session["assessmentSeleccionado"] = request.POST.get('selectorAssessment')

            context["controlesAssess"] = AssessmentCreados.objects.filter(
                assessment=request.POST.get('selectorAssessment'))
            context["usuarios"] = AsociacionUsuariosProyecto.objects.filter(
                proyecto=request.session.get('proyectoSeleccionado'))
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session["proyectoSeleccionado"]), assessment__archivado=0)
            context["marcos"] = AsociacionMarcos.objects.all()
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context=context)

        elif 'btnEditarEntrevista' in request.POST:
            entrevista = Entrevistas.objects.get(id=request.POST.get('btnEditarEntrevista'))
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSelec"] = AsociacionProyectoAssessment.objects.get(
                assessment=entrevista.assesment).proyecto.codigo
            context["proyectoSeleccionado"] = True
            request.session["proyectoSeleccionado"] = AsociacionProyectoAssessment.objects.get(
                assessment=entrevista.assesment).proyecto.codigo

            context["assessSelec"] = entrevista.assesment.id_assessment
            context["assessmentSeleccionado"] = True
            request.session["assessmentSeleccionado"] = entrevista.assesment.id_assessment

            context["entrevistaEditarEditando"] = True
            context["entrevistaEditar"] = entrevista
            context["entrevistaEditarConsultores"] = AsociacionEntrevistasUsuarios.objects.filter(
                entrevista=entrevista).values_list("usuario", flat=True)
            context["entrevistaEditarFecha"] = entrevista.fecha.replace(tzinfo=None).isoformat(timespec='minutes')
            context["entrevistaEditarDuracion"] = entrevista.duracionestimada.isoformat(timespec='minutes')
            context["entrevistaControles"] = entrevista.grupocontroles.split("\n")

            context["controlesAssess"] = AssessmentCreados.objects.filter(
                assessment=entrevista.assesment.id_assessment)
            context["usuarios"] = AsociacionUsuariosProyecto.objects.filter(
                proyecto=AsociacionProyectoAssessment.objects.get(assessment=entrevista.assesment).proyecto)
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=AsociacionProyectoAssessment.objects.get(assessment=entrevista.assesment).proyecto,
                assessment__archivado=0)
            context["marcos"] = AsociacionMarcos.objects.all()
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context=context)

        elif 'btnCrearEntrevista' in request.POST:

            controles = request.POST.getlist('selectorControles')
            grupoControles = ''
            for i in controles:
                grupoControles += i + '\n'
            if request.POST.get('Titulo') != '' and request.POST.get('Fecha') != '' and request.POST.get(
                    'Area') != '' and request.POST.get('Duracion') != '' and request.POST.get(
                'selectorEditor') != '' and grupoControles != '':
                entrevista = Entrevistas(
                    titulo=request.POST.get('Titulo'),
                    fecha=datetime.fromisoformat(request.POST.get('Fecha')),
                    grupocontroles=grupoControles,
                    area=request.POST.get('Area'),
                    creador=User.objects.get(username=request.user),
                    duracionestimada=request.POST.get('Duracion'),
                    assesment=Assessmentguardados.objects.get(
                        id_assessment=request.session.get('assessmentSeleccionado')),
                    editor=User.objects.get(username=request.POST.get('selectorEditor')),
                    asistentes=request.POST.get('Asistentes')
                )
                entrevista.save()
                users = request.POST.getlist('selectorUsuarios')
                for i in users:
                    usuario = User.objects.get(username=i)
                    asociar = AsociacionEntrevistasUsuarios(entrevista=entrevista, usuario=usuario)
                    asociar.save()
            else:
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)

            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context=context)

        elif 'btnEditarEntrevistaEnviar' in request.POST:

            controles = request.POST.getlist('selectorControles')
            grupoControles = ''
            for i in controles:
                grupoControles += i + '\n'
            if request.POST.get('Titulo') != '' and request.POST.get('Fecha') != '' and request.POST.get(
                    'Area') != '' and request.POST.get('Duracion') != '' and request.POST.get(
                'selectorEditor') != '' and grupoControles != '':
                entrevista = Entrevistas.objects.get(id=request.POST.get('btnEditarEntrevistaEnviar'))

                entrevista.titulo = request.POST.get('Titulo')
                entrevista.fecha = datetime.fromisoformat(request.POST.get('Fecha'))
                entrevista.grupocontroles = grupoControles
                entrevista.area = request.POST.get('Area')
                entrevista.creador = User.objects.get(username=request.user)
                entrevista.duracionestimada = request.POST.get('Duracion')
                entrevista.assesment = Assessmentguardados.objects.get(
                    id_assessment=request.session.get('assessmentSeleccionado'))
                entrevista.editor = User.objects.get(username=request.POST.get('selectorEditor'))
                entrevista.asistentes = request.POST.get('Asistentes')

                entrevista.save()
                users = request.POST.getlist('selectorUsuarios')
                for i in users:
                    usuario = User.objects.get(username=i)
                    asociar = AsociacionEntrevistasUsuarios(entrevista=entrevista, usuario=usuario)
                    asociar.save()
            else:
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)

            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context=context)

        elif 'btnEditarAssesment' in request.POST:
            request.session["EntrevistaEditar"] = request.POST.get('btnEditarAssesment')
            return redirect("encuestaEntrevista")
        elif 'btnEliminarEntrevista' in request.POST:
            entrevista = Entrevistas.objects.get(id=request.POST.get('btnEliminarEntrevista'))
            entrevista.delete()
            context = super(entrevistasUsuarios, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSelec"] = ''
            context["creadas"] = Entrevistas.objects.filter(editor=self.request.user)
            context["asistes"] = AsociacionEntrevistasUsuarios.objects.filter(usuario=self.request.user)
            return render(request, self.template_name, context=context)
