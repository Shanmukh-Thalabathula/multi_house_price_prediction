from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_login, name='login'),  # Default route to login page
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('recent-activities/', views.recent_activities, name='recent_activities'),
    path('delete-activity/<int:activity_id>/', views.delete_activity, name='delete_activity'),
    path('description/', views.project_description, name='description'),
]