from .__imports__ import *


class informes(LoginRequiredMixin, TemplateView):
    ''' Definición de la clase 'informes'. '''

    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/informes.html"

    # Conexión a la base de datos.
    conn = mysql.connector.connect(user='root',
                                   password="NTTCSCF2023",
                                   host='127.0.0.1',
                                   database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    def get_context_data(self, **knwargs):
        ''' El objetivo de este método es proporcionar datos de contexto para una vista,
        que luego se pueden utilizar en una plantilla HTML para renderizar la página web.'''

        # Esto inicializa un diccionario llamado context con algunos datos de contexto.
        context = super(informes, self).get_context_data(**knwargs)
        # Se guarda los assessments guardados en el contexto.
        context["assess"] = Assessmentguardados.objects.all()

        # Se devuelve el contexto.
        return context