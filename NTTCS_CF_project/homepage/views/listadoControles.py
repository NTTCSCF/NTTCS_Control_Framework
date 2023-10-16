from .__imports__ import *


class listadoControles(LoginRequiredMixin, ListView):
    ''' Definición de la clase 'listadoControles' '''

    # Define el modelo al que está asociada la vista.
    model = NttcsCf20231

    def get_queryset(self):
        ''' Obtiene el conjunto de consultas para el modelo definido. '''
        return self.model.objects.all().values()

    def get(self, request, *args, **kwargs):
        # Obtiene el valor del parámetro 'inicio' de la solicitud GET y lo convierte a un entero.
        inicio = int(request.GET.get('inicio'))
        # Obtiene el valor del parámetro 'limite' de la solicitud GET y lo convierte a un entero
        fin = int(request.GET.get('limite'))
        # Registra el tiempo de inicio de la operación
        tiempo_inicial = time()

        # Obtiene los datos del conjunto de consultas.
        data = self.get_queryset()
        # Inicializa una lista vacía para almacenar datos procesados.
        list_data = []

        # Itera sobre una porción específica de los datos.
        for indice, valor in enumerate(data[inicio: inicio + fin]):
            list_data.append(valor)

        # Calcula el tiempo total de ejecución.
        tiempo_final = time() - tiempo_inicial
        print(f'Tiempo de Ejecución: {tiempo_final}')

        # Prepara los datos a ser devueltos en la respuesta HTTP.
        data = {
            'length': data.count(),
            'object': list_data
        }

        # Devuelve una respuesta HTTP en formato JSON.
        return HttpResponse(json.dumps(data), 'application/json')