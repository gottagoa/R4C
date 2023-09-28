from django.urls import path
from . import views

urlpatterns = [
    path('create_robot/', views.create_robot, name='create_robot'),
]
