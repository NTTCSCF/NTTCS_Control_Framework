from .__imports__ import *


class Usuarios(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'Usuarios'. '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/Usuarios.html"

    def get_context_data(self, **knwargs):
        '''El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Se inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(Usuarios, self).get_context_data(**knwargs)
        # Contexto para el selector de grupos.
        context["grupos"] = Group.objects.all()
        # Contexto para el selector de usuarios.
        context["usuarios"] = User.objects.all()
        # Variable para el despliegue de la modificación de usuario.
        context["seleccionado"] = False

        # Se devuelve el contexto.
        return context

    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        # Comprobación del botón pulsado para añadir un usuario.
        if 'boton3' in request.POST:
            # Recogemos valor de selector de grupos.
            grupo = request.POST.get('selector')
            # Recogemos valor del nombre de usuario
            nUsuario = request.POST.get('nUsuario')
            # Recogemos el valor de la contraseña.
            password = request.POST.get('password')

            # Comprobación de si todos los campos están rellenados.
            if grupo != 'None' and nUsuario != '' and password != '':
                # Crear un nuevo usuario, asignarle el grupo y la contraseña proporcionados.
                usuario = User.objects.create_user(username=nUsuario, password=password, rol=grupo)
                usuario.groups.add(Group.objects.get(name__in=[grupo]))
                usuario.save()
            # Si los campos están vacíos.
            else:
                # Se crea el mensaje de error.
                messages.error(request, 'Debe rellenar todos los datos.')

        # Comprobación del selector para la funcionalidad del selector.
        elif 'selector1' in request.POST:
            # Si no se ha seleccionado ningún usuario.
            if request.POST.get('selector1') == 'None':
                '''Restablecer el contexto si no se selecciona ningún usuario.'''

                # Restablecer el contexto con información de grupos y usuarios.
                context = super(Usuarios, self).get_context_data(**knwargs)
                # Obtener todos los grupos.
                context["grupos"] = Group.objects.all()
                # Obtener todos los usuarios.
                context["usuarios"] = User.objects.all()
                # Indicar que no se ha seleccionado ningún usuario.
                context["seleccionado"] = False

                # Renderizar el template en base del contexto.
                return render(request, self.template_name, context=context)
            # Si se ha seleccionado algún usuario.
            else:
                '''Obtener información del usuario seleccionado y establecer el contexto para mostrar 
                la información del usuario.'''
                # Restablecer el contexto con información de grupos y usuarios.
                context = super(Usuarios, self).get_context_data(**knwargs)
                # Obtener todos los grupos.
                context["grupos"] = Group.objects.all()
                # Obtener todos los usuarios.
                context["usuarios"] = User.objects.all()
                # Indicar que se ha seleccionado un usuario para mostrar su información.
                context["seleccionado"] = True

                '''Obtener y configurar el usuario seleccionado y otros detalles relacionados con
                 el usuario.'''
                # Obtener el usuario seleccionado.
                usuarioSeleccionado = User.objects.get(username=request.POST.get('selector1'))
                # Pasar el usuario seleccionado al contexto.
                context["seleccion"] = usuarioSeleccionado
                # Obtener y pasar el grupo del usuario seleccionado.
                context["grupoSeleccionado"] = usuarioSeleccionado.groups.all()[0]
                # Guardar el nombre del usuario seleccionado en la sesión actual.
                request.session["usuarioSeleccionado"] = usuarioSeleccionado.username  # guardamos en la sesion el

                # Renderizar el template en base del contexto.
                return render(request, self.template_name, context=context)

        # Comprobación si hay actividad en el selector 'Seleccione un rol para el usuario'.
        elif 'selector3' in request.POST:
            # Obtener el valor del botón de 'modificar'.
            boton1 = request.POST.get('boton1')
            # Obtener el valor del selector 'Seleccione un rol para el usuario'.
            grupo = request.POST.get('selector3')
            # Valor del nUsuarioModificar.
            nUsuarioModificar = request.POST.get('nUsuarioModificar')
            # Valor del passwordModificar
            passwordModificar = request.POST.get('passwordModificar')
            # Obtener el usuario seleccionado de la sesión actual.
            user = User.objects.get(username=request.session.get('usuarioSeleccionado'))

            # Comprobar si se han rellenado todos los campos necesarios para la modificación o
            # eliminación de usuario.
            if grupo != 'None' and nUsuarioModificar != '' and nUsuarioModificar != '':
                # Comprobar si se pulsó el botón 'Modificar'.
                if boton1 == 'btn1':
                    # Actualizar el nombre de usuario.
                    user.username = nUsuarioModificar
                    # Limpiar los permisos anteriores del usuario.
                    user.groups.clear()
                    # Añadir los nuevos permisos al usuario.
                    user.groups.add(Group.objects.get(name__in=[grupo]))

                    # Comprobar si la contraseña es la contraseña hasheada
                    if passwordModificar.startswith('pbkdf2_sha256$'):
                        # Actualizar la contraseña del usuario
                        user.password = passwordModificar
                    else:
                        # Establecer una nueva contraseña para el usuario.
                        user.set_password(passwordModificar)

                    # Se guarda en la bd.
                    user.save()

                # TODO: no debería ser else if 'boton2' ?
                else:  # recogemos la pulsacion del boton Eliminar
                    user.delete()  # eliminamos el usuario seleccioando
            else:
                messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error

        context = super(Usuarios, self).get_context_data(**knwargs)
        context["grupos"] = Group.objects.all()
        context["usuarios"] = User.objects.all()
        return render(request, self.template_name, context=context)
