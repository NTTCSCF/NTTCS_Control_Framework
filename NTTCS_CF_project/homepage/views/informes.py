from .__imports__ import *

# Clase para la pagina de informes
class informes(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/informes.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')  # constante para la conexion con la base de datos

    def get_context_data(self, **knwargs):
        context = super(informes, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.all()
        return context