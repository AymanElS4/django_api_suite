from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    # return HttpResponse("¡Bienvenido a la aplicación Django!")
    return render(request, 'homepage/index.html')