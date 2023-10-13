from .__imports__ import *

# funcion utilizada para comprobar que la contraseña intruducida es correcta
def contrasenaValida(password: str) -> bool:
    largo = False  # se pone a true si la cadena es lo suficientemente larga
    mayus = False  # se pone a true si la cadena contiene una mayuscula
    numerico = False  # se pone a true si la cadena contiene un numero
    caracterEspecial = False  # se pone a true si la cadena contiene un caracter especial /\.,:;!@#$%^&*()-_=+
    if len(password) > 8:  # comprobacion de longitud
        largo = True

    for i in password:
        if i.isupper():  # comprobacion de mayus
            mayus = True
        if i.isnumeric():  # comprobacion de numero
            numerico = True
        if i in '/\.,:;!@#$%^&*()-_=+':  # comprobacion de caracter especial
            caracterEspecial = True

    return largo and mayus and numerico and caracterEspecial  # retornemos and logico entre los 4 requerimientos


# Clase para la pagina de Perfil
class Perfil(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"

    template_name = "homepage/perfil.html"

    def post(self, request, **knwargs):
        password = request.POST.get('password')  # valor del password
        passwordModificar = request.POST.get('passwordModificar')  # valor del passwordModificar
        password2Modificar = request.POST.get('password2Modificar')  # valor del password2Modificar
        user = request.user
        if password != '' and passwordModificar != '' and password2Modificar != '':  # comprobacion de entrega de cademas vacias
            if passwordModificar == password2Modificar:  # comprobacion de que las dos nuevas pass sean iguales
                if password != passwordModificar:  # coprobacion de que la contraseña nueva es distinta que la anterior
                    if user.check_password(password):  # comprobamos que la pass sea la correcta para el usuario
                        if contrasenaValida(
                                passwordModificar):  # comprobamos si la nueva pass cumple los requisitos de seguridad
                            user.set_password(passwordModificar)
                            user.save()
                            messages.success(request,
                                             'La contraseña ha sido cambiada correctamente')  # Se crea mensage de error
                        else:
                            messages.error(request,
                                           'La contraseña debe contener, 8 caracteres, alguna mayuscula, algun caracter '
                                           'especial y algun numero')  # Se crea mensage de error
                    else:
                        messages.error(request, 'La contraseña no es correcta')  # Se crea mensage de error
                else:
                    messages.error(request,
                                   'La contraseña tiene que ser distinta a la anterior')  # Se crea mensage de error
            else:
                messages.error(request, 'Las contraseñas no coinciden')  # Se crea mensage de error
        else:
            messages.error(request, 'Debe rellenar todos los datos.')  # Se crea mensage de error
        return render(request, self.template_name)
