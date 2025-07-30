from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
   path("", views.index, name="index"),
=======
   path("index/", views.index, name="index"),
>>>>>>> main
]