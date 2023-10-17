from .__imports__ import *

def contrasenaValida(password: str) -> bool:
    ''' Función utilizada para comprobar que la contraseña introducida es correcta. '''

    # Se pone a true si la cadena es lo suficientemente larga.
    largo = False
    # Se pone a true si la cadena contiene una mayúscula.
    mayus = False
    # Se pone a true si la cadena contiene un número.
    numerico = False
    # Se pone a true si la cadena contiene un carácter especial /\.,:;!@#$%^&*()-_=+
    caracterEspecial = False

    # Comprobación de longitud.
    if len(password) > 8:
        largo = True

    for i in password:
        # Comprobación de mayúsculas.
        if i.isupper():
            mayus = True
        # Comprobación de número.
        if i.isnumeric():
            numerico = True
        # Comprovación de carácter especial.
        if i in '/\.,:;!@#$%^&*()-_=+':
            caracterEspecial = True

    # Retornamos 'and' lógico entre los 4 requerimientos.
    return largo and mayus and numerico and caracterEspecial

class CreacionPass(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'creacionPass'. '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/CreacionPass.html"

    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        password = request.POST.get('password')
        ''' Valor del campo 'password'. '''

        passwordModificar = request.POST.get('passwordModificar')
        ''' Valor del campo donde se introduce la contraseña nueva. '''

        password2Modificar = request.POST.get('password2Modificar')
        ''' Valor del campo donde se introduce la contraseña nueva de nuevo. '''

        user = request.user
        ''' Obtención del usuario actual. '''

        # Comprobación de que no se han entregado cadenas vacías.
        if password != '' and passwordModificar != '' and password2Modificar != '':

            # Comprobación de que las dos nuevas contraseñas son iguales.
            if passwordModificar == password2Modificar:

                # Comprobación de que la contraseña nueva es diferente de la anterior.
                if password != passwordModificar:

                    ''' En Django, el modelo de usuario (User) proporciona el método check_password que 
                    se utiliza para verificar si la contraseña proporcionada coincide con la contraseña
                    almacenada en la base de datos para un usuario específico.'''
                    # Si la contraseña existe en la BD.
                    if user.check_password(password):

                        # Comprobamos si la nueva contraseña cumple con los requisitos de seguridad definidos
                        # en la función 'contrasenaValida'.
                        if contrasenaValida(passwordModificar):

                            # Establecer la nueva contraseña y guardar al usuario.
                            user.set_password(passwordModificar)
                            user.save()
                            messages.success(request, 'La contraseña ha sido cambiada correctamente')

                            return redirect('logout')

                        # Si la contraseña no es válida.
                        else:
                            # Se crea el mensaje de error correspondiente.
                            messages.error(request,
                                           'La contraseña debe contener, 8 caracteres, alguna mayuscula, algun caracter '
                                           'especial y algun numero')

                    # Si no es la contraseña guardada inicialmente en la bd.
                    else:
                        # Se crea el mensaje de error correspondiente.
                        messages.error(request, 'La contraseña no es correcta')

                # Si la contraseña nueva no es distinta de la anterior.
                else:
                    # Se crea el mensaje de error correspondiente.
                    messages.error(request,
                                   'La contraseña tiene que ser distinta a la anterior')
            # Si las dos contraseñas introducidas no son iguales.
            else:
                # Se crea el mensaje de error correspondiente.
                messages.error(request, 'Las contraseñas no coinciden')
        # Si no estan rellenados todos los inputs.
        else:
            # Se crea el mensaje de error correspondiente.
            messages.error(request, 'Debe rellenar todos los datos.')

        # Renderizar template sin contexto.
        return render(request, self.template_name)