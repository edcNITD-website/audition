from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Student, CQuestion, NCQuestion , Response, ClubMember, MemberFeedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
import csv
# Create your views here.
def index(request):
    return render(request, 'base/index2.html')

@login_required
def roundOne(request):
    user= request.user
    if request.method == 'POST':
        name = request.POST['name']        
        place = request.POST['place']
        branch = request.POST['branch']
        roll_number = request.POST['roll_number']
        phone_number = request.POST['phone_number']
        year = request.POST['year']
        stage = '0'
        if Student.objects.filter(user=user).first() is not None:
            s = Student.objects.get(user=user)
            s.user = user
            s.name = name
            s.place = place
            s.year = year
            s.branch = branch
            s.roll_number = roll_number
            s.phone_number = phone_number
            s.stage = '0'
            s.save(update_fields=['name', 'place', 'year', 'branch', 'roll_number', 'phone_number'])
        else:    
            student = Student.objects.create( user=user,name=name, year=year, stage=stage, branch=branch, place=place, roll_number=roll_number, phone_number=phone_number)
            student.save()
        return redirect('/round-1')

    saved_data = Student.objects.filter(user=user).first()

    core_questions = CQuestion.objects.filter(category="Core").all()
    web_questions = CQuestion.objects.filter(category="Web").all()
    gd_questions = CQuestion.objects.filter(category="GD").all()
    video_questions = CQuestion.objects.filter(category="Video").all()
    content_questions = CQuestion.objects.filter(category="Content").all()

    core_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Core").all()
    web_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Web").all()
    gd_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="GD").all()
    video_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Video").all()
    content_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Content").all()

    core_questions_new = []
    web_questions_new = []
    gd_questions_new = []
    video_questions_new = []
    content_questions_new = []

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
    
    index = 0
    for q in content_questions:
        if index < len(content_responses):
            content_questions_new.append({
                'question': q.question_text,
                'my_response': content_responses[index].question_response
            })
        else:
            content_questions_new.append({
                'question': q.question_text,
                'my_response': ""
            })
        index = index + 1

    context = {
        'saved_data': saved_data,
        'core_questions': core_questions_new,
        'web_questions': web_questions_new,
        'gd_questions': gd_questions_new,
        'video_questions': video_questions_new,
        'content_questions': content_questions_new
    }
    return render (request, 'base/form2.html', context)

def profile(request):
    return render(request, 'base/profile2.html')

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
        category = request.POST['category']
        Response.objects.filter(student=member, category=category).all().delete()
        for i in range(1,len(Cquestions)+1):
            response= "response"+str(i)
            if response in request.POST:
                ans = request.POST[response]
                Response.objects.create(student = student[0], question_text = Cquestions[i-1].question_text, question_response = ans, student_phone_number= phone_number, student_name = name, category=category)
                
            else:
                pass

        return redirect('/round-1')    

    core_questions = CQuestion.objects.filter(category="Core").all()
    web_questions = CQuestion.objects.filter(category="Web").all()
    gd_questions = CQuestion.objects.filter(category="GD").all()
    video_questions = CQuestion.objects.filter(category="Video").all()
    content_questions = CQuestion.objects.filter(category="Content").all()

    core_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Core").all()
    web_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Web").all()
    gd_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="GD").all()
    video_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Video").all()
    content_responses = Response.objects.filter(student=Student.objects.filter(user=request.user).first(), category="Content").all()

    core_questions_new = []
    web_questions_new = []
    gd_questions_new = []
    video_questions_new = []
    content_questions_new = []

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
    
    index = 0
    for q in content_questions:
        if index < len(content_responses):
            content_questions_new.append({
                'question': q.question_text,
                'my_response': content_responses[index].question_response
            })
        else:
            content_questions_new.append({
                'question': q.question_text,
                'my_response': ""
            })
        index = index + 1

    context = {
        'core_questions': core_questions_new,
        'web_questions': web_questions_new,
        'gd_questions': gd_questions_new,
        'video_questions': video_questions_new,
        'content_questions': content_questions_new
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
    return render(request, 'base/results2.html')

def members(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        user = request.POST['user']
        member_feedback = MemberFeedback(member=ClubMember.objects.filter(user=request.user).first(), student=Student.objects.filter(user=User.objects.filter(username=user).first()).first())
        member_feedback.feedback = feedback
        member_feedback.save()
        return redirect('/members')
    else:
        if request.user.is_authenticated and ClubMember.objects.filter(user=request.user).first() is not None:
            students = Student.objects.all()
            data = []
            no_of_students = Student.objects.all().count()
            applied_for_gd = 0
            applied_for_webd = 0
            applied_for_video = 0
            applied_for_content = 0
            for student in students:
                resposne = Response.objects.filter(student=student).all()
                all_feedback = MemberFeedback.objects.filter(student=student).all()
                member_feedback = MemberFeedback.objects.filter(student=student, member=ClubMember.objects.filter(user=request.user).first()).first()
                student_responses = Response.objects.filter(student=student)
                domain = set()
                for student_response in student_responses:
                    domain.add(student_response.category)
                    da = ""
                    for d in domain:
                        if d == 'Web':
                            applied_for_webd += 1
                        if d == 'Content':
                            applied_for_content += 1
                        if d == 'Video':
                            applied_for_video += 1
                        if d == 'GD':
                            applied_for_gd += 1
                context = []
                context.append({
                    'no_of_students': no_of_students,
                    'applied_for_gd': applied_for_gd,
                    'applied_for_webd': applied_for_webd,
                    'applied_for_video': applied_for_video,
                    'applied_for_content': applied_for_content
                })

                data.append({
                    'student': student,
                    'resposne': resposne,
                    'all_feedback': all_feedback,
                    'member_feedback': member_feedback
                })
            return render(request, 'base/members.html', { 'data': data, 'statistics': context })
        else:
            return redirect('/')       

def isSelected(request):
    if request.method == "POST" and request.user.is_authenticated and ClubMember.objects.filter(user=request.user).first() is not None:
        student = Student.objects.filter(user=User.objects.filter(username=request.POST['user']).first()).first()
        student.stage = request.POST['stage']
        student.save()
        return redirect('/members')

def nextRoundCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        max_round = 0
        for student in students:
            if max_round < int(student.stage):
                max_round = int(student.stage)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="result.csv"'
        writer = csv.writer(response)
        writer.writerow(
                [
                    "Round " + str(max_round),
                ]
            )
        writer.writerow([])
        writer.writerow(
                [
                    "Student",
                    "Phone Number"
                ]
            )
        for student in students:
            if int(student.stage) == max_round:
                writer.writerow(
                [
                    student.name,
                    student.phone_number
                ]
            )
        return response
    else:
        return redirect('/')

def allStudentsCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students.csv"'
        writer = csv.writer(response)
        writer.writerow(
                [
                    "Name",
                    "Branch",
                    "Roll Number",
                    "Place",
                    "Phone Number",
                    "Email",
                    "Domain"
                ]
            )
        for student in students:
            student_responses = Response.objects.filter(student=student)
            domain = set()
            for student_response in student_responses:
                domain.add(student_response.category)
            da = ""
            for d in domain:
                if d != 'Core':
                    da = da + d + " "
            writer.writerow(
                [
                    student.name,
                    student.branch,
                    student.roll_number,
                    student.place,
                    student.phone_number,
                    student.user.email,
                    da
                ]
            )
        return response
    else:
        return redirect('/')

def studentResponseCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="responses.csv"'
        writer = csv.writer(response)
        writer.writerow(
                [
                    "Name",
                    "Phone Number",
                    "Question",
                    "Category",
                    "Response"
                ]
            )
        for student in students:
            student_responses = Response.objects.filter(student=student)
            writer.writerow(
                [
                    student.name,
                    student.phone_number
                ]
            )
            for student_response in student_responses:
                writer.writerow(
                    [
                        "",
                        "",
                        student_response.question_text,
                        student_response.category,
                        student_response.question_response
                    ]
                )
            writer.writerow([])
        return response
    else:
        return redirect('/')
