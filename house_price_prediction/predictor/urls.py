from django.urls import path
from . import views

urlpatterns = [
    path('predict/<str:city>', views.predict_price, name='predict_price'),
]
