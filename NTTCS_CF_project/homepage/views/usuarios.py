from .__imports__ import *

# Clase para la pagina de Usuarios
class Usuarios(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/Usuarios.html"

    def get_context_data(self, **knwargs):
        context = super(Usuarios, self).get_context_data(**knwargs)
        context["grupos"] = Group.objects.all()  # contexto para el selector de gupos
        context["usuarios"] = User.objects.all()  # contexto para el selector de usuarios
        context["seleccionado"] = False  # variable para el despliegue de la modificacion de usuario
        return context

    def post(self, request, **knwargs):

        if 'boton3' in request.POST:  # if que recoge la pulsacion del boton de añadir usuario
            grupo = request.POST.get('selector')  # recogemos valor de selector de grupos
            nUsuario = request.POST.get('nUsuario')  # recogemos valor del nombre de usuario
            password = request.POST.get('password')  # recogemos el valor de la contraseña

            if grupo != 'None' and nUsuario != '' and password != '':  # comprobamos si todas las casillas esta rellenas.
                usuario = User.objects.create_user(username=nUsuario, password=password,
                                                   rol=grupo)  # creamos el usuario
                usuario.groups.add(Group.objects.get(name__in=[grupo]))  # le añadimos los permisos
                usuario.save()  # guardamos el usuario
            else:
                messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error

        elif 'selector1' in request.POST:  # if para la funcionalidad del selector
            if request.POST.get('selector1') == 'None':  # comprobamos si se selecciona el No Seleccionado
                context = super(Usuarios, self).get_context_data(**knwargs)
                context["grupos"] = Group.objects.all()
                context["usuarios"] = User.objects.all()
                context["seleccionado"] = False  # fijamos el desplegable a false
                return render(request, self.template_name, context=context)
            else:
                context = super(Usuarios, self).get_context_data(**knwargs)
                context["grupos"] = Group.objects.all()
                context["usuarios"] = User.objects.all()
                context["seleccionado"] = True  # fijamos el desplegable a true para que se muestre la info del usuario.
                usuarioSeleccionado = User.objects.get(username=request.POST.get('selector1'))  # fijamos el usuario
                context["seleccion"] = usuarioSeleccionado  # pasamos el usuario
                context["grupoSeleccionado"] = usuarioSeleccionado.groups.all()[0]  # pasamos el grupo del usuario
                # seleccionado
                request.session["usuarioSeleccionado"] = usuarioSeleccionado.username  # guardamos en la sesion el
                # usuario que se ha seleccioando.
                print(usuarioSeleccionado.password)
                return render(request, self.template_name, context=context)
        elif 'selector3' in request.POST:  # Recogemos el valor de los botones de modificar y eliminar.
            boton1 = request.POST.get('boton1')  # valor del boton 1
            grupo = request.POST.get('selector3')  # valor del boton 1
            nUsuarioModificar = request.POST.get('nUsuarioModificar')  # valor del nUsuarioModificar
            passwordModificar = request.POST.get('passwordModificar')  # valor del passwordModificar
            user = User.objects.get(username=request.session.get('usuarioSeleccionado'))  # recogemos el usuario
            # seleccionado en la sesion.
            if grupo != 'None' and nUsuarioModificar != '' and nUsuarioModificar != '':  # comprobamos que se hayan
                # rellenado todos los campos
                if boton1 == 'btn1':  # recogemos la pulsacion del boton modificar
                    user.username = nUsuarioModificar  # fijamos el nombre del usuario
                    user.groups.clear()  # limpiamos los permisos anteriores
                    user.groups.add(Group.objects.get(name__in=[grupo]))  # añadimos los nuevos permisos, pueden ser
                    # los mismos
                    if passwordModificar.startswith('pbkdf2_sha256$'):  # comprobamos si el valor de la contraseña es
                        # la hasheada, osea la anterior, no podemos saber el valor sin hashear
                        user.password = passwordModificar
                    else:  # si no es el valor hasheado lo tenemos que encriptar
                        user.set_password(passwordModificar)  # para eso usamos el set_password
                    user.save()
                else:  # recogemos la pulsacion del boton Eliminar
                    user.delete()  # eliminamos el usuario seleccioando
            else:
                messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error

        context = super(Usuarios, self).get_context_data(**knwargs)
        context["grupos"] = Group.objects.all()
        context["usuarios"] = User.objects.all()
        return render(request, self.template_name, context=context)
