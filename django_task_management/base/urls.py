from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('label/<str:id>', views.label, name="label"),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status')
]