from django.urls import path
from . import views

urlpatterns = [
    path('generate_robot_summary_excel/', views.generate_robot_summary_excel, name='generate_robot_summary_excel'),
    path('generate_robot_summary_csv/', views.generate_robot_summary_csv, name='generate_robot_summary_csv'),
]