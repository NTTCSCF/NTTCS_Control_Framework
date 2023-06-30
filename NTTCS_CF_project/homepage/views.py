from django.shortcuts import render, HttpResponse, redirect
from .models import Assessment, MaturirtyTable, AsociacionMarcos, Assessmentguardados, Assessment, SeleccionAssessment, \
    NttcsCf20231,FrameworkList,Domains,EvidenceRequestCatalog
from django.views.generic import TemplateView
import mysql.connector
from django.contrib.sessions.backends.db import SessionStore


# Create your views here.


class index(TemplateView):
    template_name = "homepage/index.html"

    def post(self, request):
        user = request.POST.get('usuario')
        pas = request.POST.get('pass')

        if user == 'eloy' and pas == '1234':
            return render(request, 'homepage/menu.html')
        return render(request, self.template_name)


class assessment(TemplateView):
    template_name = "homepage/assessment.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')
    assSelect = SeleccionAssessment.objects.get(seleccion='assessmentSeleccionado').valor

    def get_context_data(self, **knwargs):

        context = super(assessment, self).get_context_data(**knwargs)
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + self.assSelect)
        context["assess"] = mycursor
        context["valMad"] = MaturirtyTable.objects.all()
        return context

    def post(self, request, **knwargs):
        select = request.POST.get('selector')
        boton = request.POST.get('boton')
        boton2 = request.POST.get('boton2')
        boton3 = request.POST.get('boton3')

        if boton == 'btn1':
            consulta = Assessment.objects.get(id=select)
            context = super(assessment, self).get_context_data(**knwargs)
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + self.assSelect)
            context["assess"] = mycursor
            context["valMad"] = MaturirtyTable.objects.all()
            context["opciones"] = consulta
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + self.assSelect + " WHERE ID='" + select + "'")
            for fila in mycursor:
                context["respuesta"] = fila[4]
                context["valoracion"] = fila[5]
            return render(request, self.template_name, context=context)

        elif boton2 == 'btn2':
            consulta = Assessment.objects.get(id=select)
            query = """UPDATE """ + self.assSelect + """ SET descripcion='""" + consulta.control_description + """', 
            pregunta='""" + consulta.control_question + """', criterioValoracion='', respuesta='""" + \
                    request.POST.get('respuesta') + """', valoracion='""" + request.POST.get('valmad') + """', 
                    evidencia='' WHERE ID='""" + consulta.id + """';"""
            mycursor = self.conn.cursor()
            mycursor.execute(query)
            self.conn.commit()
        else:
            consulta = Assessmentguardados.objects.get(id_assessment=self.assSelect)
            consulta.archivado = 1
            consulta.save()
            return redirect('menu')
        context = super(assessment, self).get_context_data(**knwargs)
        mycursor = self.conn.cursor(buffered=True)
        mycursor.execute("SELECT * FROM " + self.assSelect)
        context["assess"] = mycursor
        return render(request, self.template_name, context=context)


class assessmentselect(TemplateView):
    template_name = "homepage/assessmentselect.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    def get_context_data(self, **knwargs):
        context = super(assessmentselect, self).get_context_data(**knwargs)
        context["assess"] = Assessmentguardados.objects.all()
        context["marcos"] = AsociacionMarcos.objects.all()
        return context

    def post(self, request, **knwargs):
        nombre = request.POST.get('in')
        select = request.POST.get('selector1')
        select2 = request.POST.getlist('selector2')
        if select != 'none':
            assSelect = SeleccionAssessment.objects.get(seleccion='assessmentSeleccionado')
            assSelect.valor = select
            assSelect.save()
            return redirect("assessment")
        elif nombre != '' and select2 != None:
            query = '''CREATE TABLE ''' + nombre + ''' (
                                ID varchar(100) NOT NULL,
                                descripcion text NULL,
                                pregunta text NULL,
                                criterioValoracion text NULL,
                                respuesta text NULL,
                                valoracion text NULL,
                                evidencia text NULL,
                                CONSTRAINT NewTable_pk PRIMARY KEY (ID)
                            )
                            ENGINE=InnoDB
                            DEFAULT CHARSET=utf8mb4
                            COLLATE=utf8mb4_0900_ai_ci;'''
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute(query)

            marcos = ''
            marc = []
            mycursor = self.conn.cursor(buffered=True)
            for i in select2:

                mycursor.execute("SELECT * FROM " + AsociacionMarcos.objects.get(marco_id=i).nombre_tabla)
                for fila in mycursor:
                    if fila[0] not in marc:
                        marc += [fila[0]]

            for marco in marc:
                marcos += marco + '\n'
                mycursor = self.conn.cursor(buffered=True)
                query = """INSERT INTO """ + nombre + """(ID, descripcion, pregunta, criterioValoracion, respuesta, valoracion, evidencia) VALUES('""" + str(
                    marco) + """', '', '', '', '', '', '');"""
                mycursor.execute(query)

            self.conn.commit()

            self.conn.close()

            c = Assessmentguardados(id_assessment=nombre, marcos=marcos)
            c.save()
            assSelect = SeleccionAssessment.objects.get(seleccion='assessmentSeleccionado')
            assSelect.valor = nombre
            assSelect.save()
            return redirect("assessment")
        else:
            context = super().get_context_data(**knwargs)
            context["assess"] = Assessmentguardados.objects.all()
            context["marcos"] = AsociacionMarcos.objects.all()
            return render(request, self.template_name, context=context)


class Exportaciones(TemplateView):
    template_name = "homepage/Exportaciones.html"


class informes(TemplateView):
    template_name = "homepage/informes.html"


class Mantenimiento(TemplateView):
    template_name = "homepage/Mantenimiento.html"


class MantenimientoNivelMadurez(TemplateView):
    template_name = "homepage/MantenimientoNivelMadurez.html"

    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')

            if busqueda == '':
                context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
                context["consulta"] = MaturirtyTable.objects.all()
                context["lenConsulta"] = len(MaturirtyTable.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = MaturirtyTable.objects.get(sublevels=busqueda)
                context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})
                context["lenConsulta"] = 1
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('Sublevels') != None:
            Ccmmcod = request.POST.get('Ccmmcod')
            Description = request.POST.get('Description')
            Sublevels = request.POST.get('Sublevels')
            Percentage = request.POST.get('Percentage')

            try:
                consulta = MaturirtyTable.objects.get(sublevels=Sublevels)
                consulta.ccmmcod = Ccmmcod
                consulta.description = Description
                consulta.percentage = Percentage
                consulta.save()
            except:
                insert = MaturirtyTable(ccmmcod=Ccmmcod, description=Description, sublevels=Sublevels,
                                        percentage=Percentage)
                insert.save()

            context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
            context["consulta"] = MaturirtyTable.objects.all()
            context["lenConsulta"] = len(MaturirtyTable.objects.all())
            return render(request, self.template_name, context=context)

        else:
            consulta = MaturirtyTable.objects.get(sublevels=request.session["ultBusqueda"])

            context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
            context["consulta"] = MaturirtyTable.objects.all()
            context["lenConsulta"] = len(MaturirtyTable.objects.all())
            context["seleccion"] = consulta
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoNivelMadurez, self).get_context_data(**knwargs)
        context["consulta"] = MaturirtyTable.objects.all()
        context["lenConsulta"] = len(MaturirtyTable.objects.all())
        return context

    def Eliminar(request):

        consulta = MaturirtyTable.objects.get(sublevels=request.session["ultBusqueda"])
        consulta.delete()

        return redirect('mantenimientoNivelMadurez')


class menu(TemplateView):
    template_name = "homepage/menu.html"


class MantenimientoDominios(TemplateView):
    template_name = "homepage/MantenimientoDominios.html"
    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')

            if busqueda == '':
                context = super(MantenimientoDominios, self).get_context_data(**knwargs)
                context["consulta"] = Domains.objects.all()
                context["lenConsulta"] = len(Domains.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = Domains.objects.get(identifier=busqueda)
                context = super(MantenimientoDominios, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})
                context["lenConsulta"] = 1
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('identifier') is not None:
            identifier = request.POST.get('identifier')
            domain = request.POST.get('domain')
            security_privacy_by_design_s_p_principles = request.POST.get('security_privacy_by_design_s_p_principles')
            principle_intent = request.POST.get('principle_intent')


            try:
                consulta = Domains.objects.get(identifier=identifier)
                consulta.domain = domain
                consulta.security_privacy_by_design_s_p_principles = security_privacy_by_design_s_p_principles
                consulta.principle_intent = principle_intent
                consulta.save()

            except:
                insert = Domains(identifier=identifier, domain=domain, security_privacy_by_design_s_p_principles=security_privacy_by_design_s_p_principles, principle_intent=principle_intent,)
                insert.save()

            context = super(MantenimientoDominios, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            return render(request, self.template_name, context=context)

        else:
            consulta = Domains.objects.get(identifier=request.session["ultBusqueda"])
            context = super(MantenimientoDominios, self).get_context_data(**knwargs)
            context["consulta"] = Domains.objects.all()
            context["lenConsulta"] = len(Domains.objects.all())
            context["seleccion"] = consulta
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoDominios, self).get_context_data(**knwargs)
        context["consulta"] = Domains.objects.all()
        context["lenConsulta"] = len(Domains.objects.all())
        return context

    def Eliminar(request):

        consulta = Domains.objects.get(identifier=request.session["ultBusqueda"])
        consulta.delete()

        return redirect('MantenimientoDominios')

class MantenimientoEvidencias(TemplateView):
    template_name = "homepage/MantenimientoEvidencias.html"
    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')

            if busqueda == '':
                context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
                context["consulta"] = EvidenceRequestCatalog.objects.all()
                context["lenConsulta"] = len(EvidenceRequestCatalog.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = EvidenceRequestCatalog.objects.get(evidence_request_references=busqueda)
                context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})
                context["lenConsulta"] = 1
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('evidence_request_references') != None:
            evidence_request_references = request.POST.get('evidence_request_references')
            area_of_focus = request.POST.get('area_of_focus')
            artifact = request.POST.get('artifact')
            artifact_description = request.POST.get('artifact_description')
            control_mappings = request.POST.get('control_mappings')

            try:
                consulta = EvidenceRequestCatalog.objects.get(evidence_request_references=evidence_request_references)
                consulta.area_of_focus = area_of_focus
                consulta.artifact = artifact
                consulta.artifact_description = artifact_description
                consulta.control_mappings = control_mappings
                consulta.save()
            except:
                insert = EvidenceRequestCatalog(evidence_request_references=evidence_request_references, area_of_focus=area_of_focus, artifact=artifact,
                                        artifact_description=artifact_description,control_mappings=control_mappings)
                insert.save()

            context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
            context["consulta"] = EvidenceRequestCatalog.objects.all()
            context["lenConsulta"] = len(EvidenceRequestCatalog.objects.all())
            return render(request, self.template_name, context=context)

        else:
            consulta = EvidenceRequestCatalog.objects.get(evidence_request_references=request.session["ultBusqueda"])

            context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
            context["consulta"] = EvidenceRequestCatalog.objects.all()
            context["lenConsulta"] = len(EvidenceRequestCatalog.objects.all())
            context["seleccion"] = consulta
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoEvidencias, self).get_context_data(**knwargs)
        context["consulta"] = EvidenceRequestCatalog.objects.all()
        context["lenConsulta"] = len(EvidenceRequestCatalog.objects.all())
        return context

    def Eliminar(request):

        consulta = EvidenceRequestCatalog.objects.get(evidence_request_references=request.session["ultBusqueda"])
        consulta.delete()

        return redirect('MantenimientoEvidencias')

class MantenimientoPreguntas(TemplateView):
    template_name = "homepage/MantenimientoPreguntas.html"
    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')

            if busqueda == '':
                context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
                context["consulta"] = Assessment.objects.all()
                context["lenConsulta"] = len(Assessment.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = Assessment.objects.get(id=busqueda)
                context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})
                context["lenConsulta"] = 1
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('id') != None:
            control_question = request.POST.get('control_question')
            control_description = request.POST.get('control_description')
            id = request.POST.get('id')

            try:
                consulta = Assessment.objects.get(id=id)
                consulta.control_description = control_description
                consulta.control_question = control_question
                consulta.save()
            except:
                insert = Assessment(id=id, control_question=control_question, control_description=control_description)
                insert.save()

            context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
            context["consulta"] = Assessment.objects.all()
            context["lenConsulta"] = len(Assessment.objects.all())
            return render(request, self.template_name, context=context)

        else:
            consulta = Assessment.objects.get(id=request.session["ultBusqueda"])

            context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
            context["consulta"] = Assessment.objects.all()
            context["lenConsulta"] = len(Assessment.objects.all())
            context["seleccion"] = consulta
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoPreguntas, self).get_context_data(**knwargs)
        context["consulta"] = Assessment.objects.all()
        context["lenConsulta"] = len(Assessment.objects.all())
        return context

    def Eliminar(request):

        consulta = Assessment.objects.get(id=request.session["ultBusqueda"])
        consulta.delete()

        return redirect('MantenimientoPreguntas')

class MantenimientoMarcosExistentes(TemplateView):
    template_name = "homepage/MantenimientoMarcosExistentes.html"

    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')

            if busqueda == '':
                context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
                context["consulta"] = AsociacionMarcos.objects.all()
                context["lenConsulta"] = len(AsociacionMarcos.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = AsociacionMarcos.objects.get(marco_id=busqueda)
                context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})
                context["lenConsulta"] = 1
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('framework_id') != None:
            marco_id = request.POST.get('marco_id')
            nombre_tabla = request.POST.get('nombre_tabla')



            try:
                consulta = AsociacionMarcos.objects.get(marco_id=marco_id)
                consulta.nombre_tabla = nombre_tabla

                consulta.save()

            except:
                insert = AsociacionMarcos(marco_id=marco_id, nombre_tabla=nombre_tabla)
                insert.save()

            context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
            context["consulta"] = AsociacionMarcos.objects.all()
            context["lenConsulta"] = len(AsociacionMarcos.objects.all())
            return render(request, self.template_name, context=context)

        else:
            consulta = AsociacionMarcos.objects.get(marco_id=request.session["ultBusqueda"])
            context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
            context["consulta"] = AsociacionMarcos.objects.all()
            context["lenConsulta"] = len(AsociacionMarcos.objects.all())
            context["seleccion"] = consulta
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoMarcosExistentes, self).get_context_data(**knwargs)
        context["consulta"] = AsociacionMarcos.objects.all()
        context["lenConsulta"] = len(AsociacionMarcos.objects.all())
        return context

    def Eliminar(request):

        consulta = AsociacionMarcos.objects.get(marco_id=request.session["ultBusqueda"])
        consulta.delete()

        return redirect('MantenimientoMarcosExistentes')

class MantenimientoControlesNTTCS(TemplateView):
    template_name = "homepage/MantenimientoControlesNTTCS.html"

    def post(self, request, **knwargs):

        if request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')

            if busqueda == '':
                context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
                context["consulta"] = NttcsCf20231.objects.all()
                context["lenConsulta"] = len(NttcsCf20231.objects.all())
                return render(request, self.template_name, context=context)
            else:
                consulta = NttcsCf20231.objects.get(id=busqueda)
                context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
                context.update({'consulta': consulta})
                context["lenConsulta"] = 1
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('id') != None:
            domain = request.POST.get('domain')
            selected_y_n_field = request.POST.get('selected_y_n_field')
            control = request.POST.get('control')
            id = request.POST.get('id')
            control_description = request.POST.get('control_description')
            relative_control_weighting = request.POST.get('relative_control_weighting')
            function_grouping = request.POST.get('function_grouping')
            assesed_result = request.POST.get('assesed_result')
            numeric_result = request.POST.get('numeric_result')
            weighted_numeric_result = request.POST.get('weighted_numeric_result')
            assessment_comments = request.POST.get('assessment_comments')
            relative_result_by_function = request.POST.get('relative_result_by_function')
            relative_result_by_domain = request.POST.get('relative_result_by_domain')

            try:
                consulta = NttcsCf20231.objects.get(id=id)
                consulta.domain = domain
                consulta.selected_y_n_field = selected_y_n_field
                consulta.control = control
                consulta.control_description = control_description
                consulta.relative_control_weighting = relative_control_weighting
                consulta.function_grouping = function_grouping
                consulta.assesed_result = assesed_result
                consulta.numeric_result = numeric_result
                consulta.weighted_numeric_result = weighted_numeric_result
                consulta.assessment_comments = assessment_comments
                consulta.relative_result_by_function = relative_result_by_function
                consulta.relative_result_by_domain = relative_result_by_domain
                consulta.save()
            except:
                insert = NttcsCf20231(domain=domain, selected_y_n_field=selected_y_n_field,id=id, control=control,
                                      control_description=control_description,
                                      relative_control_weighting=relative_control_weighting,
                                      function_grouping=function_grouping, assesed_result=assesed_result,
                                      numeric_result=numeric_result, weighted_numeric_result=weighted_numeric_result,
                                      assessment_comments=assessment_comments,
                                      relative_result_by_function=relative_result_by_function,
                                      relative_result_by_domain=relative_result_by_domain)
                insert.save()

            context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
            context["consulta"] = NttcsCf20231.objects.all()
            context["lenConsulta"] = len(NttcsCf20231.objects.all())
            return render(request, self.template_name, context=context)

        else:
            consulta = NttcsCf20231.objects.get(id=request.session["ultBusqueda"])
            context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
            context["consulta"] = NttcsCf20231.objects.all()
            context["lenConsulta"] = len(NttcsCf20231.objects.all())
            context["seleccion"] = consulta
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoControlesNTTCS, self).get_context_data(**knwargs)
        context["consulta"] = NttcsCf20231.objects.all()
        context["lenConsulta"] = len(NttcsCf20231.objects.all())
        return context

    def Eliminar(request):

        consulta = NttcsCf20231.objects.get(id=request.session["ultBusqueda"])
        consulta.delete()

        return redirect('MantenimientoControlesNTTCS')
class MantenimientoMapeoMarcos(TemplateView):
    template_name = "homepage/MantenimientoMapeoMarcos.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')

    def get_context_data(self, **knwargs):
        context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
        context["assess"] = AsociacionMarcos.objects.all()
        context["consulta"] = [['no seleccionado', 'no seleccionado']]
        context["lenConsulta"] = 1
        return context


    def post(self, request, **knwargs):
        boton1 = request.POST.get('boton1')

        if boton1 == 'btn1':
            selector = request.POST.get('selectorMapeo')
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + AsociacionMarcos.objects.get(marco_id=selector).nombre_tabla)
            context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
            context["assess"] = AsociacionMarcos.objects.all()
            context["consulta"] = mycursor
            context["lenConsulta"] = 5
            request.session["seleccion"] = AsociacionMarcos.objects.get(marco_id=selector).nombre_tabla
            return render(request, self.template_name, context=context)

        elif request.POST.get('busqueda') is not None:
            busqueda = request.POST.get('busqueda')
            if busqueda == '':
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + request.session["seleccion"])
                context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
                context["assess"] = AsociacionMarcos.objects.all()
                context["consulta"] = mycursor
                return render(request, self.template_name, context=context)
            else:
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + request.session["seleccion"]+" WHERE ID='" + busqueda + "'")
                context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
                context["assess"] = AsociacionMarcos.objects.all()
                context["consulta"] = mycursor
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)
        elif request.POST.get('marco_id') != None:
            id = request.POST.get('id')
            marco_id = request.POST.get('marco_id')
            nombre_tabla = request.POST.get('nombre_tabla')

            try:
                query = "UPDATE "+request.session["seleccion"]+" SET NTT_ID='"+marco_id+"', "+request.session["seleccion"]+"='"+nombre_tabla+"' WHERE ID="+id+";"
                mycursor = self.conn.cursor()
                mycursor.execute(query)
                self.conn.commit()
            except:
                query = "INSERT INTO "+request.session["seleccion"]+" (NTT_ID, "+request.session["seleccion"]+") VALUES('"+marco_id+"', '"+nombre_tabla+"');"

                mycursor = self.conn.cursor()
                mycursor.execute(query)
                self.conn.commit()

            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + request.session["seleccion"])
            context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
            context["assess"] = AsociacionMarcos.objects.all()
            context["consulta"] = mycursor
            return render(request, self.template_name, context=context)

        else:

            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + request.session["seleccion"] + " WHERE ID='" + request.session["ultBusqueda"] + "'")
            context = super(MantenimientoMapeoMarcos, self).get_context_data(**knwargs)
            context["assess"] = AsociacionMarcos.objects.all()
            context["consulta"] = mycursor
            for o in mycursor:
                context["seleccion"] = o
            return render(request, self.template_name, context=context)



    def EliminarMapeo(request):
        conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                       auth_plugin='mysql_native_password')
        mycursor = conn.cursor(buffered=True)
        mycursor.execute(
            "DELETE FROM " + request.session["seleccion"] + " WHERE ID='" + request.session["ultBusqueda"] + "';")
        conn.commit()
        conn.close()
        return redirect('MantenimientoMapeoMarcos')



class MantenimientoAssessmentArchivados(TemplateView):
    template_name = "homepage/MantenimientoAssessmentArchivados.html"
    conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                   auth_plugin='mysql_native_password')
    def post(self, request, **knwargs):
        boton = request.POST.get('boton')
        if boton == 'btn1':
            selector = request.POST.get('selector')
            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + selector)
            context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
            s = Assessmentguardados.objects.all()
            p = []
            for i in s:
                if i.archivado == 1:
                    p += [i]
            context["selector"] = p
            context["consulta"] = mycursor
            request.session["seleccion"] = selector
            return render(request, self.template_name, context=context)
        elif request.POST.get('busqueda') != None:
            busqueda = request.POST.get('busqueda')
            print(busqueda)
            if busqueda == '':
                mycursor = self.conn.cursor(buffered=True)
                mycursor.execute("SELECT * FROM " + request.session["seleccion"])
                context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
                s = Assessmentguardados.objects.all()
                p = []
                for i in s:
                    if i.archivado == 1:
                        p += [i]
                context["selector"] = p
                context["consulta"] = mycursor
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)
            else:
                mycursor = self.conn.cursor(buffered=True)
                query = "SELECT * FROM " + request.session["seleccion"]+" WHERE ID='" + busqueda + "'"
                mycursor.execute(query)
                context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
                s = Assessmentguardados.objects.all()
                p = []
                for i in s:
                    if i.archivado == 1:
                        p += [i]
                context["selector"] = p
                context["consulta"] = mycursor
                request.session["ultBusqueda"] = busqueda
                return render(request, self.template_name, context=context)

        elif request.POST.get('id') != None:
            id = request.POST.get('id')
            descripcion = request.POST.get('descripcion')
            Pregunta = request.POST.get('Pregunta')
            criterio = request.POST.get('criterio')
            respuesta = request.POST.get('respuesta')
            valoracion = request.POST.get('valoracion')
            evidencia = request.POST.get('evidencia')

            try:
                query = """UPDATE """ + request.session["seleccion"]+ """ SET descripcion='""" + descripcion + """', 
                            pregunta='""" + Pregunta + """', criterioValoracion='"""+criterio+"""', respuesta='""" + \
                        respuesta + """', valoracion='""" + valoracion + """', 
                                    evidencia='"""+evidencia+"""' WHERE ID='""" + id + """';"""
                mycursor = self.conn.cursor()
                mycursor.execute(query)
                self.conn.commit()
            except:
                query = """INSERT INTO """ + request.session["seleccion"] + """(ID, descripcion, pregunta, criterioValoracion, respuesta, valoracion, evidencia) VALUES('""" + id + """', '""" + descripcion + """', '""" + Pregunta + """', '""" + criterio + """', '""" + respuesta + """', '""" + valoracion + """', '""" + evidencia + """');"""
                mycursor = self.conn.cursor()
                mycursor.execute(query)
                self.conn.commit()

            mycursor = self.conn.cursor(buffered=True)
            mycursor.execute("SELECT * FROM " + request.session["seleccion"])
            context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
            s = Assessmentguardados.objects.all()
            p = []
            for i in s:
                if i.archivado == 1:
                    p += [i]
            context["selector"] = p
            context["consulta"] = mycursor
            return render(request, self.template_name, context=context)

        else:
            mycursor = self.conn.cursor(buffered=True)
            query = "SELECT * FROM " + request.session["seleccion"] + " WHERE ID='" + request.session["ultBusqueda"] + "'"
            mycursor.execute(query)
            context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
            s = Assessmentguardados.objects.all()
            p = []
            for i in s:
                if i.archivado == 1:
                    p += [i]
            context["selector"] = p
            context["consulta"] = mycursor
            for o in mycursor:
                context["seleccion"] = o
            return render(request, self.template_name, context=context)

    def get_context_data(self, **knwargs):
        context = super(MantenimientoAssessmentArchivados, self).get_context_data(**knwargs)
        s = Assessmentguardados.objects.all()
        p = []
        for i in s:
            if i.archivado == 1:
                p += [i]
        context["selector"] = p
        context["consulta"] = [['No Seleccionado', 'No Seleccionado', 'No Seleccionado', 'No Seleccionado', 'No Seleccionado', 'No Seleccionado', 'No Seleccionado']]

        return context

    def EliminarAssessment(request):
        conn = mysql.connector.connect(user='root', password="NTTCSCF2023", host='127.0.0.1', database='nttcs_cf',
                                       auth_plugin='mysql_native_password')
        mycursor = conn.cursor(buffered=True)
        mycursor.execute("DELETE FROM "+request.session["seleccion"]+" WHERE ID='"+request.session["ultBusqueda"] +"';")
        conn.commit()
        conn.close()
        return redirect('MantenimientoAssessmentArchivados')