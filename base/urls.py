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
    path('all-students', views.allStudents, name="allStudents"),
    path('is-selected', views.isSelected, name="isSelected"),
    path('nextRoundCSV', views.nextRoundCSV, name="nextRoundCSV"),
    path('allStudentsCSV', views.allStudentsCSV, name="allStudentsCSV"),
    path('techStudentsCSV', views.techStudentsCSV, name="techStudentsCSV"),
    path('webStudentsCSV', views.webStudentsCSV, name="webStudentsCSV"),
    path('allUserExceptStudentsCSV', views.allUserExceptStudentsCSV, name="allUserExceptStudentsCSV"),
    path('studentResponseCSV', views.studentResponseCSV, name="studentResponseCSV"),
    path('rejectedStudentsCSV', views.rejectedStudentsCSV, name="rejectedStudentsCSV"),
    path('student/<str:slug>', views.studentId, name="studentId"),
]
