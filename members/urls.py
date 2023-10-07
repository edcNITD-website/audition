from django.urls import path,include
from . import views


urlpatterns = [
    path('login/', views.memberlogin),
    path('', views.dashboard, name= "dashboard"),
    path('students/', views.dashboard, name= "students"),
    path('questions/', views.questions, name= "member_questions"),
    path('questions/add/', views.add, name= "add"),
    path('questions/edit/<int:id>/', views.edit, name= "edit"),
    path('questions/delete/<int:id>', views.delete, name= "delete"),
]