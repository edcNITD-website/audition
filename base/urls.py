from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('questions/', views.questions, name='questions'),
    path('export', views.export, name='export'),
    path('results', views.results, name="results"),
    

    
]
