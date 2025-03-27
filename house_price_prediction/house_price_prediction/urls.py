from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('predictor/', include('predictor.urls')),
    path('', include('users.urls')),
    path('visualization/', include('visualization.urls')),
]