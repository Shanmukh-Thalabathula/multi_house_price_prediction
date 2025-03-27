# descriptive_statistics/urls.py
from django.urls import path
from . import views

app_name = 'descriptive_statistics'

urlpatterns = [
    path('<str:city>/', views.descriptive_stats, name='descriptive_stats'),
]