from .__imports__ import *


class index(LoginView):
    ''' Definición de la clase 'index'. '''

    template_name = "homepage/index.html"

    def post(self, request):
        ''' Método usado para manejar solcitudes HTTP POST enviadas por el cliente, en este caso,
        a través de un formulario.'''

        # Obtener el nombre de usuario.
        user = request.POST.get('user')
        # Obtener la contraseña.
        pas = request.POST.get('pass')
        # Autenticar al usuario utilizando el método 'authenticate' de Django.
        usuario = authenticate(request, username=user, password=pas)

        # Comprobación de si el usuario se autentica correctamente.
        if usuario is not None:
            # Si es la primera vez que el usuario inicia sesión, redirigir a la vista 'creacionPass'.
            if usuario.last_login is None:
                login(request, usuario)

                return redirect('creacionPass')

            # Si el usuario ya ha iniciado sesión anteriormente, redirigir a la vista 'menu'.
            else:
                login(request, usuario)

                return redirect('menu')
        # Si la autenticación falla, renderizar la plantilla de inicio de sesión nuevamente.
        else:
            return render(request, self.template_name)

# Decorator que requiere que el usuario esté autenticado para acceder a la función 'logout'
@login_required
def logout(request):
    # Cerrar la sesión del usuario utilizando el método 'logout' de Django
    logout(request)
    # Redirigir al usuario a la página de inicio.
    return redirect('/')


