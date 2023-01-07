from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Student(models.Model):
    user = models.ForeignKey( User, null=True, blank=False ,on_delete= models.CASCADE)
    # WEBD GD CONTENT PHOTOGRAPHY
    stage = models.CharField(max_length=1)
    branch = models.CharField(max_length= 100, blank=False)
    roll_number= models.CharField(max_length=8, null=True, blank=False)
    place = models.CharField(max_length=100, null=True, blank=False)
    name = models.CharField(max_length=500, null=True, blank=False)
    phone_number = models.CharField(max_length=10, null=True, blank=False)
    year = models.CharField(max_length= 1, default= '2', null=True )
    

    def __str__(self):
        return self.name
# C - Compulsory
class CQuestion(models.Model):
    student = models.ForeignKey( Student, null=True, blank=False, on_delete=models.CASCADE)
    #remove student's response if he/she gets removed from db
    question_text = models.CharField(max_length=500, blank=False, null=True)
    question_response = models.CharField(max_length=2000, blank=False, null=True)

    def __str__(self):
        return self.question_text

class NCQuestion(models.Model):
    student = models.ForeignKey( Student, null=True, blank=False, on_delete=models.CASCADE)
    #remove student's response if he/she gets removed from db
    question_text = models.CharField(max_length=500, blank=False, null=True)
    question_response = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.question_text



class Response(models.Model):
    student = models.ForeignKey( Student, null=True, blank=False, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=500 , null=True )
    student_phone_number = models.CharField(max_length=10, null=True)
    #remove student's response if he/she gets removed from db
    question_text = models.CharField(max_length=500, blank=False, null=True)
    question_response = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return str(self.student) + str(self.question_text)
        

# Admin Functionality
class ClubMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class MemberFeedback(models.Model):
    member = models.ForeignKey(ClubMember, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    def __str__(self):
        return self.member.user.first_name + " " + self.member.user.last_name + " | " + self.student.user.first_name + " " + self.student.user.last_name