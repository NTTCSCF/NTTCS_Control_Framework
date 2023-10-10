from .__imports__ import *

# Clase para la pagina de Exportaciones
class Exportaciones(LoginRequiredMixin, TemplateView):
    login_url = ""
    redirect_field_name = "redirect_to"
    template_name = "homepage/Exportaciones.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')  # constante para la conexion con la base de datos

    def get_context_data(self, **knwargs):
        context = super(Exportaciones, self).get_context_data(**knwargs)
        context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
        return context

    # funcion post que recoge los summit del formulario de la pagina.
    def post(self, request, **knwargs):
        selectorProyecto = request.POST.get('selectorProyecto')  # valor de selector de proyecto
        selector = request.POST.get('selector1')
        excel = request.POST.get('excel')
        csvinput = request.POST.get('csv')
        word = request.POST.get('word')
        if 'selectorProyecto' in request.POST:
            context = super(Exportaciones, self).get_context_data(**knwargs)
            context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
            context["proyectoSelec"] = selectorProyecto
            context["proyectoSeleccionado"] = True
            request.session["proyectoSeleccionado"] = selectorProyecto
            context["assess"] = AsociacionProyectoAssessment.objects.filter(
                proyecto=Proyecto.objects.get(codigo=selectorProyecto), assessment__archivado=0)
            context["marcos"] = AsociacionMarcos.objects.all()
            return render(request, self.template_name, context=context)
        elif "selector1" in request.POST:
            if selector != 'None':
                ass = Assessmentguardados.objects.get(id_assessment=selector)
                consulta = AssessmentCreados.objects.filter(assessment=ass)
                seleccion = request.POST.getlist("selector2")
                valores = []

                for fila in consulta:  # Rellenamos tanto las casillas de respuesta y valoracion
                    evgen = AsociacionEvidenciasGenericas.objects.filter(assessment=fila)
                    evcre = AsociacionEvidenciasCreadas.objects.filter(id_assessment=fila)
                    evidencias = ''
                    iniciativas = ''
                    for i in evgen:
                        if ass.idioma == 'en':
                            evidencias += i.evidencia.evidence_request_references + '\n'
                        else:
                            evidencias += i.evidencia_id_es.evidence_request_references + '\n'
                        if i.iniciativa != None:
                            iniciativas += i.iniciativa.nombre + '\n'
                    for i in evcre:
                        evidencias += i.id_evidencia.evidencia_id + '\n'
                        if i.iniciativa != None:
                            iniciativas += i.iniciativa.nombre + '\n'

                    valor = []

                    if "Identificador Control" in seleccion:
                        valor += [('Identificador Control', fila.control_id)]
                    if "Nombre Control" in seleccion:
                        valor += [('Nombre Control', fila.control_name)]
                    if "Descripcion Control" in seleccion:
                        valor += [('Descripcion Control', fila.descripcion)]
                    if "Pregunta" in seleccion:
                        valor += [('Pregunta', fila.pregunta)]
                    if "Respuesta" in seleccion:
                        if fila.respuesta == None:
                            valor += [('Respuesta', fila.respuesta)]
                        else:
                            valor += [('Respuesta', BeautifulSoup(fila.respuesta, "lxml").text)]
                            print(BeautifulSoup(fila.respuesta, "lxml").text)
                    if "Valoracion" in seleccion:
                        valor += [('Valoracion', fila.valoracion)]
                    if "Valoracion Objetivo" in seleccion:
                        valor += [('Valoracion Objetivo', fila.valoracionobjetivo)]
                    if "Evidencias" in seleccion:
                        valor += [('Evidencias', evidencias)]
                    if "Iniciativas" in seleccion:
                        valor += [('Iniciativas', iniciativas)]

                    valores += dict(valor),
                titulos = []
                for i in seleccion:
                    titulos += [i]
                now = datetime.now()
                filename = 'Exportaciones/' + selector + '_Export_' + str(now.day) + '_' + str(now.month) + '_' + str(
                    now.year) + '_' + str(now.hour) + '_' + str(now.minute)
                if 'csv' == csvinput:
                    filename += '.csv'
                    with open(filename, mode='w', encoding="cp437", errors="replace") as file:
                        writer = csv.DictWriter(file, delimiter=',', fieldnames=titulos)
                        writer.writeheader()

                        for valor in valores:
                            writer.writerow(valor)

                    path = open(filename, 'r')
                    mime_type, _ = mimetypes.guess_type(filename)
                    response = HttpResponse(path, content_type=mime_type)
                    response['Content-Disposition'] = f"attachment; filename={filename}"
                    return response

                if 'excel' == excel:
                    filename += '.xlsx'

                    df = pd.DataFrame(data=valores)
                    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
                    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']
                    column_settings = [{'header': column} for column in df.columns]
                    (max_row, max_col) = df.shape
                    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
                    worksheet.autofilter(0, 0, max_row, max_col - 1)
                    cell_format = workbook.add_format()
                    cell_format.set_text_wrap()
                    worksheet.set_column('A:I', 20, cell_format)
                    writer.close()

                    with open(filename, "rb") as file:
                        response = HttpResponse(file.read(),
                                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                        response['Content-Disposition'] = f"attachment; filename={filename}"
                    return response

                if 'word' == word:
                    filename += '.docx'
                    # create document object
                    document = Document()

                    for i in valores:
                        document.add_heading(i['Identificador Control'] + ", " + i['Nombre Control'], level=1)
                        table = document.add_table(rows=0, cols=2)
                        table.style = 'TableGrid'
                        for j in titulos:

                            row_cells = table.add_row().cells
                            row_cells[0].text = j

                            if i[j] != None:
                                row_cells[1].text = i[j]
                            else:
                                row_cells[1].text = ""
                        p = document.add_paragraph('')
                    # save document
                    document.save(filename)
        context = super(Exportaciones, self).get_context_data(**knwargs)
        context["proyectos"] = AsociacionUsuariosProyecto.objects.filter(usuario=self.request.user)
        return render(request, self.template_name, context=context)
