from django.shortcuts import render
<<<<<<< HEAD


# Create your views here.
from django.http import HttpResponse

def index(request):
=======
from django.http import HttpResponse

# Create your views here.

def index(request):
    # return HttpResponse("¡Bienvenido a la aplicación Django!")
>>>>>>> main
    return render(request, 'homepage/index.html')