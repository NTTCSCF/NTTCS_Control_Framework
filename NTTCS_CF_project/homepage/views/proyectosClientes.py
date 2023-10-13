from .__imports__ import *

class proyectosClientes(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/proyectosClientes.html"

    def get_context_data(self, **knwargs):
        context = super(proyectosClientes, self).get_context_data(**knwargs)
        context["clientes"] = Cliente.objects.all()
        context["proyectos"] = Proyecto.objects.all()
        context["usuarios"] = User.objects.all()

        return context

    def post(self, request, **knwargs):

        if 'selectorCliente' in request.POST:
            context = super(proyectosClientes, self).get_context_data(**knwargs)
            context["clientes"] = Cliente.objects.all()
            context["usuarios"] = User.objects.all()
            context["clienteSeleccionado"] = True
            context["proyectos"] = Proyecto.objects.all()
            context["cliente"] = Cliente.objects.get(codigo=request.POST.get('selectorCliente'))
            return render(request, self.template_name,
                          context=context)  # siempre retornamos el valor con la tabla completa.

        elif 'codigo' in request.POST:
            if request.POST["codigo"] != '' and request.POST["nombre"] != '':
                if not Cliente.objects.filter(codigo=request.POST["codigo"]).exists():
                    cliente_nuevo = Cliente(codigo=request.POST["codigo"],
                                            nombre=request.POST["nombre"],
                                            logo=request.FILES['logo']
                                            )
                    cliente_nuevo.save()

                else:
                    messages.error(request, 'ERROR, el Cliente ya existe de id ya existe')
            else:
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')


        elif 'selectorProyecto' in request.POST:
            context = super(proyectosClientes, self).get_context_data(**knwargs)
            context["clientes"] = Cliente.objects.all()
            context["usuarios"] = User.objects.all()
            context["proyectoSeleccionado"] = True
            context["proyectos"] = Proyecto.objects.all()
            a = AsociacionUsuariosProyecto.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.POST.get('selectorProyecto')))
            p = []
            for i in a:
                p += [i.usuario.username]
            context["usuariosProyecto"] = p
            request.session['selectorProyecto'] = request.POST.get('selectorProyecto')
            context["proyecto"] = Proyecto.objects.get(codigo=request.POST.get('selectorProyecto'))
            return render(request, self.template_name,
                          context=context)  # siempre retornamos el valor con la tabla completa.
        elif 'codigoProyecto' in request.POST:
            codigo = request.POST.get('codigoProyecto')
            nombre = request.POST.get('nombreProyecto')
            descripcion = request.POST.get('descripcionProyecto')
            cliente = request.POST.get('selectorClienteProyecto')
            usuarios = request.POST.getlist('selectorUsuarios')
            if codigo != '' and nombre != '' and descripcion != '' and cliente is not None:
                if not Proyecto.objects.filter(codigo=codigo).exists():
                    cliente = Cliente.objects.get(codigo=cliente)
                    proyecto = Proyecto(codigo=codigo, nombre=nombre, descripcion=descripcion, cliente=cliente,
                                        fecha_creacion=datetime.now())
                    proyecto.save()
                    for i in usuarios:
                        user = User.objects.get(username=i)
                        asosciacion = AsociacionUsuariosProyecto(usuario=user, proyecto=proyecto)
                        asosciacion.save()
                else:
                    messages.error(request, 'ERROR, el Proyecto ya existe')
            else:
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            context = super(proyectosClientes, self).get_context_data(**knwargs)
            context["clientes"] = Cliente.objects.all()
            context["usuarios"] = User.objects.all()
            context["proyectos"] = Proyecto.objects.all()

            return render(request, self.template_name,
                          context=context)
        elif 'selectorUsuarios2' in request.POST:
            usuarios = request.POST.getlist('selectorUsuarios2')
            proyecto = Proyecto.objects.get(codigo=request.session.get('selectorProyecto'))
            aso = AsociacionUsuariosProyecto.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session.get('selectorProyecto')))
            aso.delete()

            for i in usuarios:
                user = User.objects.get(username=i)
                asosciacion = AsociacionUsuariosProyecto(usuario=user, proyecto=proyecto)
                asosciacion.save()

            context = super(proyectosClientes, self).get_context_data(**knwargs)
            context["clientes"] = Cliente.objects.all()
            context["usuarios"] = User.objects.all()
            context["proyectoSeleccionado"] = True
            context["proyectos"] = Proyecto.objects.all()
            a = AsociacionUsuariosProyecto.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session.get('selectorProyecto')))
            p = []
            for i in a:
                p += [i.usuario.username]
            context["usuariosProyecto"] = p

            context["proyecto"] = Proyecto.objects.get(codigo=request.session.get('selectorProyecto'))
            return render(request, self.template_name,
                          context=context)  # siempre retornamos el valor con la tabla completa.

        context = super(proyectosClientes, self).get_context_data(**knwargs)
        context["clientes"] = Cliente.objects.all()
        context["usuarios"] = User.objects.all()
        context["proyectos"] = Proyecto.objects.all()
        return render(request, self.template_name,
                      context=context)  # siempre retornamos el valor con la tabla completa.
