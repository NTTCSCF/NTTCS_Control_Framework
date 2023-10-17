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

class Perfil(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'Perfil' '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/perfil.html"

    def post(self, request, **knwargs):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario. '''

        # Se obtienen los valores de los campos 'password' del objeto request.
        password = request.POST.get('password')
        # Se obtienen los valores de los campos 'passwordModificar' del objeto request.
        passwordModificar = request.POST.get('passwordModificar')
        # Se obtienen los valores de los campos 'password2Modificar' del objeto request.
        password2Modificar = request.POST.get('password2Modificar')
        # Se obtiene el usuario actual
        user = request.user

        # Comprobación de que los campos no están vacíos.
        if password != '' and passwordModificar != '' and password2Modificar != '':

            # Comprobación de que los dos nuevos passwords son iguales.
            if passwordModificar == password2Modificar:

                # Comprobación de que la contraseña nueva es distinta de la anterior
                if password != passwordModificar:

                    # Comprobación de que la contraseña actual ingresada por el usuario es la correspondiente en la bd.
                    if user.check_password(password):

                        '''Comprobación de si la nueva contraseña cumple con los requisitos de seguridad 
                        usando la función contrasenaValida.'''
                        if contrasenaValida(passwordModificar):
                            # Se establece la nueva contraseña para el usuario.
                            user.set_password(passwordModificar)
                            # Se guarda en la bd.
                            user.save()
                            # Se crea mensaje de éxito.
                            messages.success(request, 'La contraseña ha sido cambiada correctamente')

                        # Si no cumple los requisitos de la contraseña.
                        else:
                            # Se crea mensaje de error.
                            messages.error(request,
                                           'La contraseña debe contener, 8 caracteres, alguna mayuscula, algun caracter '
                                           'especial y algun numero')
                    # Si la contraseña no es igual a la que hay en la bd.
                    else:
                        # Se crea mensaje de error.
                        messages.error(request, 'La contraseña no es correcta')

                # Si la contraseña es igual a la anterior.
                else:
                    # Se crea mensaje de error.
                    messages.error(request,
                                   'La contraseña tiene que ser distinta a la anterior')

            # Si las contraseñas no coinciden.
            else:
                # Se crea mensaje de error.
                messages.error(request, 'Las contraseñas no coinciden')

        # Si algún campo está vacío.
        else:
            # Se crea mensaje de error.
            messages.error(request, 'Debe rellenar todos los datos.')

        # Se renderiza el template.
        return render(request, self.template_name)
