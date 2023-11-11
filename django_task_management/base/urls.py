from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('label/<str:id>', views.label, name="label"),

]