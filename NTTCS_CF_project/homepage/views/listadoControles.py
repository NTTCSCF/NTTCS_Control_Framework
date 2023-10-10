from .__imports__ import *


class listadoControles(LoginRequiredMixin, ListView):
    model = NttcsCf20231

    def get_queryset(self):
        return self.model.objects.all().values()

    def get(self, request, *args, **kwargs):
        inicio = int(request.GET.get('inicio'))
        fin = int(request.GET.get('limite'))
        tiempo_inicial = time()
        data = self.get_queryset()
        list_data = []
        for indice, valor in enumerate(data[inicio: inicio + fin]):
            list_data.append(valor)
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución: {tiempo_final}')

        data = {
            'length': data.count(),
            'object': list_data
        }

        return HttpResponse(json.dumps(data), 'application/json')