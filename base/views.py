from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Student, CQuestion, NCQuestion , Response, ClubMember, MemberFeedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
import csv
# Create your views here.
def index(request):
    return render(request, 'base/index.html')

@login_required
def register(request):
    
     # stage    year
    user= request.user
    context={

     }
    if request.method == 'POST':
        name = request.POST['name']        
        place = request.POST['place']
        branch = request.POST['branch']
        roll_number = request.POST['roll_number']
        phone_number = request.POST['phone_number']
        year = request.POST['year']
    
        
        stage = '0'
        user = user
        student = Student.objects.create( user=user,name=name, year=year, stage=stage, branch=branch, place=place, roll_number=roll_number, phone_number=phone_number)
        student.save()
        return redirect('index')
    # context={
    #     'student':student,

    # }
        

    return render (request, 'base/form.html') 


def profile(request):
    
    return render(request, 'base/profile.html')

@login_required
def questions(request):
    
    user = request.user
    student = Student.objects.filter(user=user)
    member = student[0]
    phone_number = member.phone_number

    name = member.name


    Cquestions= CQuestion.objects.all()
    NCquestions = NCQuestion.objects.all()

    for i in range(1,len(Cquestions)+1):
        response= "response"+str(i)
        if response in request.POST:
            ans = request.POST[response]
            
            Response.objects.create(student = student[0], question_text = Cquestions[i-1].question_text, question_response = ans, student_phone_number= phone_number, student_name = name)
            
        else:
            pass
            

 
     
    
    context={
        'cquestions': Cquestions,
        'ncquestions': NCquestions,
    }

    
    return render (request, 'base/questions.html', context)
    return HttpResponse("hey")

def export(request):
    students = Student.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename= results.csv'
    Cquestions= CQuestion.objects.all()
    NCquestions = NCQuestion.objects.all()
    fields = ['ID','Student Name', 'Phone Number']
    # now have to add all questions as a field
    for question in Cquestions:
        fields.append(str(question.question_text))
    for question in NCquestions:
        fields.append(str(question.question_text))
    writer = csv.writer(response)
    writer.writerow(fields)
    student_fields = students.values_list('pk','name', 'phone_number')
    for student in students:
        student_fields = students.values_list('name', 'phone_number')
        Canswers = CQuestion.objects.filter(student = student)
        NCanswers = NCQuestion.objects.filter(student = student)
        student_fields.append(Canswers.values_list('question_response'))
        student_fields.append(NCanswers.values_list('question_response'))
        writer.writerow(student)
    return response





def results(request):
    return render(request, 'base/results.html')

def members(request):
    if request.user.is_authenticated and ClubMember.objects.filter(user=request.user).first() is not None:
        students = Student.objects.all()
        data = []
        for student in students:
            resposne = Response.objects.filter(student=student).all()
            data.append({
                'student': student,
                'resposne': resposne
            })
        return render(request, 'base/members.html', { 'data': data })
    else:
        return redirect('/')