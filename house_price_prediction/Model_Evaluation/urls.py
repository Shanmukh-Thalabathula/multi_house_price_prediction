from django.urls import path
from . views import *
urlpatterns = [
    path('model-metrics/', model_metrics, name='model-metrics'),
]