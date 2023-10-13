from .__imports__ import *

# Clase para la pagina del login
class index(LoginView):
    template_name = "homepage/index.html"

    def post(self, request):
        user = request.POST.get('user')
        pas = request.POST.get('pass')
        usuario = authenticate(request, username=user, password=pas)

        if usuario is not None:
            if usuario.last_login is None:
                login(request, usuario)
                return redirect('creacionPass')
            else:
                login(request, usuario)
                return redirect('menu')

        else:
            return render(request, self.template_name)


@login_required
def logout(request):
    logout(request)
    return redirect('/')


