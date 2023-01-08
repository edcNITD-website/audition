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
        if Student.objects.filter(user=user).first() is not None:
            Student.objects.filter(user=user).first().delete()
        student = Student.objects.create( user=user,name=name, year=year, stage=stage, branch=branch, place=place, roll_number=roll_number, phone_number=phone_number)
        student.save()
        return redirect('index')
    # context={
    #     'student':student,

    # }

    saved_data = Student.objects.filter(user=user).first()

    return render (request, 'base/form.html', { 'saved_data': saved_data })


def profile(request):
    
    return render(request, 'base/profile.html')

@login_required
def questions(request):
    if request.method == 'POST':
        user = request.user
        student = Student.objects.filter(user=user)
        member = student.first()
        phone_number = member.phone_number

        name = member.name


        Cquestions= CQuestion.objects.all()
        NCquestions = NCQuestion.objects.all()
        # Response.objects.filter(student=member).all().delete()
        category = request.POST['category']
        Response.objects.filter(student=member, category=category).all().delete()
        for i in range(1,len(Cquestions)+1):
            response= "response"+str(i)
            if response in request.POST:
                ans = request.POST[response]
                Response.objects.create(student = student[0], question_text = Cquestions[i-1].question_text, question_response = ans, student_phone_number= phone_number, student_name = name, category=category)
                
            else:
                pass

        return redirect('/questions')    

 
     
    # my_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first())
    # c_questions = CQuestion.objects.all()
    # nc_questions = NCQuestion.objects.all()
    # c_questions_new = []
    # nc_questions_new = []
    # context = {}
    # index = 0
    # for q in c_questions:
        # if index < len(my_responses):
        #     c_questions_new.append({
        #         'question': q.question_text,
        #         'my_response': my_responses[index].question_response
        #     })
        # else:
        #     c_questions_new.append({
        #         'question': q.question_text,
        #         'my_response': ""
        #     })
        # index = index + 1
    # context={
    #     'cquestions': c_questions_new,
    #     'ncquestions': NCQuestion.objects.all()
    # }

    core_questions = CQuestion.objects.filter(category="Core").all()
    web_questions = CQuestion.objects.filter(category="Web").all()
    gd_questions = CQuestion.objects.filter(category="GD").all()
    video_questions = CQuestion.objects.filter(category="Video").all()

    core_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Core").all()
    web_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Web").all()
    gd_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="GD").all()
    video_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Video").all()

    core_questions_new = []
    web_questions_new = []
    gd_questions_new = []
    video_questions_new = []

    index = 0
    for q in core_questions:
        if index < len(core_responses):
            core_questions_new.append({
                'question': q.question_text,
                'my_response': core_responses[index].question_response
            })
        else:
            core_questions_new.append({
                'question': q.question_text,
                'my_response': ""
            })
        index = index + 1

    index = 0
    for q in web_questions:
        if index < len(web_responses):
            web_questions_new.append({
                'question': q.question_text,
                'my_response': web_responses[index].question_response
            })
        else:
            web_questions_new.append({
                'question': q.question_text,
                'my_response': ""
            })
        index = index + 1

    index = 0
    for q in gd_questions:
        if index < len(gd_responses):
            gd_questions_new.append({
                'question': q.question_text,
                'my_response': gd_responses[index].question_response
            })
        else:
            gd_questions_new.append({
                'question': q.question_text,
                'my_response': ""
            })
        index = index + 1

    index = 0
    for q in video_questions:
        if index < len(video_responses):
            video_questions_new.append({
                'question': q.question_text,
                'my_response': video_responses[index].question_response
            })
        else:
            video_questions_new.append({
                'question': q.question_text,
                'my_response': ""
            })
        index = index + 1

    context = {
        'core_questions': core_questions_new,
        'web_questions': web_questions_new,
        'gd_questions': gd_questions_new,
        'video_questions': video_questions_new 
    }
    return render (request, 'base/questions.html', context)

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