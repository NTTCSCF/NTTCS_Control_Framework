from .__imports__ import *

class proyectosClientes(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'proyectosClientes' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/proyectosClientes.html"

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(proyectosClientes, self).get_context_data(**knwargs)
        # Obtener todos los clientes.
        context["clientes"] = Cliente.objects.all()
        # Obtener todos los proyectos.
        context["proyectos"] = Proyecto.objects.all()
        # Obtener todos los usuarios.
        context["usuarios"] = User.objects.all()

        return context

    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        # Se comprueba si se ha seleccionado un cliente que se quiera visualizar.
        if 'selectorCliente' in request.POST:
            # Obtiene el contexto de la superclase.
            context = super(proyectosClientes, self).get_context_data(**knwargs)
            # Se obtiene todos los clientes de la bd.
            context["clientes"] = Cliente.objects.all()
            # Se obtiene todos los usuarios de la bd.
            context["usuarios"] = User.objects.all()
            # Se obtiene todos los proyectos de la bd.
            context["proyectos"] = Proyecto.objects.all()
            # Establece la variable de 'clienteSeleccionado' en True, cosa que renderizará un trozo de vista.
            context["clienteSeleccionado"] = True
            # Obtiene el cliente específico basado en el código proporcionado en la solicitud POST.
            context["cliente"] = Cliente.objects.get(codigo=request.POST.get('selectorCliente'))

            # Renderiza un template en base de la bd.
            return render(request, self.template_name, context=context)

        # Comprueba si se ha enviado información para crear un nuevo cliente.
        elif 'codigo' in request.POST:
            # Verifica si los campos 'codigo' y 'nombre' no están vacíos.
            if request.POST["codigo"] != '' and request.POST["nombre"] != '':
                # Comprueba si ya existe un cliente con el mismo código en la base de datos.
                if not Cliente.objects.filter(codigo=request.POST["codigo"]).exists():
                    # Crea un nuevo cliente con los datos proporcionados en la solicitud POST.
                    cliente_nuevo = Cliente(codigo=request.POST["codigo"],
                                            nombre=request.POST["nombre"],
                                            logo=request.FILES['logo'])
                    # Se guarda en la bd.
                    cliente_nuevo.save()

                # Si el cliente existe en la bd.
                else:
                    # Se crea un mensaje de error.
                    messages.error(request, 'ERROR, el Cliente ya existe de id ya existe')
            # Si los campos están vacíos.
            else:
                # Se crea un mensaje de error.
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

        # Comprueba si se ha seleccionado un proyecto específico.
        elif 'selectorProyecto' in request.POST:
            # Obtiene el contexto de la superclase.
            context = super(proyectosClientes, self).get_context_data(**knwargs)
            # Obtiene todos los clientes de la bd.
            context["clientes"] = Cliente.objects.all()
            # Obtiene todos los usuarios de la bd.
            context["usuarios"] = User.objects.all()
            # Establece la variable de 'proyectoSeleccionado' en True, cosa que renderizará un trozo de vista.
            context["proyectoSeleccionado"] = True
            # Se obtiene todos los proyectos de la bd.
            context["proyectos"] = Proyecto.objects.all()
            # Obtiene la asociación de usuarios para el proyecto seleccionado.
            a = AsociacionUsuariosProyecto.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.POST.get('selectorProyecto')))

            '''Se guarda en una lista los usuarios asociados al proyecto.'''
            p = []
            for i in a:
                p += [i.usuario.username]

            # Agrega los nombres de usuario al contexto.
            context["usuariosProyecto"] = p
            # Almacena el proyecto seleccionado en la sesión.
            request.session['selectorProyecto'] = request.POST.get('selectorProyecto')
            # Obtiene el proyecto específico basado en el código proporcionado en la solicitud POST.
            context["proyecto"] = Proyecto.objects.get(codigo=request.POST.get('selectorProyecto'))

            # Se renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        # Comprueba si se han proporcionado datos para crear un nuevo proyecto.
        elif 'codigoProyecto' in request.POST:
            ''' Obtiene los datos del proyecto del formulario.'''
            codigo = request.POST.get('codigoProyecto')
            nombre = request.POST.get('nombreProyecto')
            descripcion = request.POST.get('descripcionProyecto')
            cliente = request.POST.get('selectorClienteProyecto')
            usuarios = request.POST.getlist('selectorUsuarios')

            # Verifica si los campos necesarios no están vacíos.
            if codigo != '' and nombre != '' and descripcion != '' and cliente is not None:
                # Comprueba si ya existe un proyecto con el mismo código en la base de datos.
                if not Proyecto.objects.filter(codigo=codigo).exists():
                    # Obtiene el cliente relacionado con el proyecto.
                    cliente = Cliente.objects.get(codigo=cliente)
                    # Crea un nuevo objeto de Proyecto con los datos proporcionados.
                    proyecto = Proyecto(codigo=codigo, nombre=nombre, descripcion=descripcion, cliente=cliente,
                                        fecha_creacion=datetime.now())
                    # Guardar el proyecto en la bd.
                    proyecto.save()

                    '''Asocia los usuarios seleccionados con el proyecto y se guarda en la bd.'''
                    for i in usuarios:
                        user = User.objects.get(username=i)
                        asosciacion = AsociacionUsuariosProyecto(usuario=user, proyecto=proyecto)
                        asosciacion.save()

                # Si el proyecto ya existe en la bd.
                else:
                    # Se crea un mensaje de error.
                    messages.error(request, 'ERROR, el Proyecto ya existe')
            # Si los campos están vacíos.
            else:
                # Se crea un mensaje de error.
                messages.error(request, 'ERROR, Necesitas introducir todos los valores')

            '''Actualiza el contexto con los datos relevantes de la base de datos.'''
            context = super(proyectosClientes, self).get_context_data(**knwargs)
            context["clientes"] = Cliente.objects.all()
            context["usuarios"] = User.objects.all()
            context["proyectos"] = Proyecto.objects.all()

            # Se renderiza el remplate en base del contexto.
            return render(request, self.template_name, context=context)

        # Comprueba si se han seleccionado usuarios específicos para un proyecto.
        elif 'selectorUsuarios2' in request.POST:
            # Obtiene la lista de usuarios seleccionados del formulario.
            usuarios = request.POST.getlist('selectorUsuarios2')
            # Obtiene el proyecto correspondiente a partir de la sesión.
            proyecto = Proyecto.objects.get(codigo=request.session.get('selectorProyecto'))
            # Obtiene las asociaciones de usuarios para el proyecto seleccionado.
            aso = AsociacionUsuariosProyecto.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session.get('selectorProyecto')))
            # Elimina la asociación.
            aso.delete()

            ''' Asocia los usuarios seleccionados con el proyecto y los guarda en la base de datos.'''
            for i in usuarios:
                user = User.objects.get(username=i)
                asosciacion = AsociacionUsuariosProyecto(usuario=user, proyecto=proyecto)
                asosciacion.save()

            # Obtiene el contexto de la superclase.
            context = super(proyectosClientes, self).get_context_data(**knwargs)
            # Se obtiene todos los clientes de la bd.
            context["clientes"] = Cliente.objects.all()
            # Se obtiene todos los usuarios de la bd.
            context["usuarios"] = User.objects.all()
            # Establece la variable de 'proyectoSeleccionado' en True, cosa que renderizará un trozo de vista.
            context["proyectoSeleccionado"] = True
            # Se obtiene todos los proyectos de la bd.
            context["proyectos"] = Proyecto.objects.all()
            # Obtiene las asociaciones de usuarios para el proyecto seleccionado y obtiene los nombres de usuario.
            a = AsociacionUsuariosProyecto.objects.filter(
                proyecto=Proyecto.objects.get(codigo=request.session.get('selectorProyecto')))

            '''Se guarda en una lista los usuarios asociados al proyecto.'''
            p = []
            for i in a:
                p += [i.usuario.username]

            # Agrega los nombres de usuario al contexto.
            context["usuariosProyecto"] = p
            # Agrega el proyecto seleccionado al contexto.
            context["proyecto"] = Proyecto.objects.get(codigo=request.session.get('selectorProyecto'))

            # Se renderiza el template en base del contexto.
            return render(request, self.template_name, context=context)

        ''' En caso de que no se presione nada, 'default'. '''
        # Obtiene el contexto de la superclase.
        context = super(proyectosClientes, self).get_context_data(**knwargs)
        # Se obtiene todos los clientes de la bd.
        context["clientes"] = Cliente.objects.all()
        # Se obtiene todos los usuarios de la bd.
        context["usuarios"] = User.objects.all()
        # Se obtiene todos los proyectos de la bd.
        context["proyectos"] = Proyecto.objects.all()

        # Se renderiza el template en base del contexto.
        return render(request, self.template_name, context=context)
