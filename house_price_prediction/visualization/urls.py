from django.urls import path
from . import views

urlpatterns = [
    path('visualize/<str:city>/', views.area_prices, name='visualize'),
]
