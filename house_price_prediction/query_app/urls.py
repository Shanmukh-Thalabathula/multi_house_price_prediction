from django.urls import path
from . import views

urlpatterns = [
    path('query/', views.query_interface, name='query_interface'),
]