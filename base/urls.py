from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('round-1', views.roundOne, name='roundOne'),
    path('profile/', views.profile, name='profile'),
    path('questions/', views.questions, name='questions'),
    path('export', views.export, name='export'),
    path('results', views.results, name="results"),
    path('members', views.members, name="members"),
    path('is-selected', views.isSelected, name="isSelected"),
    path('nextRoundCSV', views.nextRoundCSV, name="nextRoundCSV"),
    path('allStudentsCSV', views.allStudentsCSV, name="allStudentsCSV"),
    path('studentResponseCSV', views.studentResponseCSV, name="studentResponseCSV"),
]
