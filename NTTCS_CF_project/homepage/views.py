from django.shortcuts import render

# Create your views here.

def index(request):
    user = request.POST.get('usuario')
    passw = request.POST.get('pass')

    if user == 'Eloy' and passw == '1234':
        return render(request, 'homepage/menu.html')

    return render(request, 'homepage/index.html')

def assessment(request):
    return render(request, 'homepage/assessment.html')

def assessmentselect(request):
    return render(request, 'homepage/assessmentselect.html')

def Exportaciones(request):
    return render(request, 'homepage/Exportaciones.html')

def informes(request):
    return render(request, 'homepage/informes.html')

def Mantenimiento(request):
    if request.method == "POST":
        print('buenas tardes')
    return render(request, 'homepage/Mantenimiento.html')

def menu(request):

    return render(request, 'homepage/menu.html')

def prueba():
    print('buenas tardes')

