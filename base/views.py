from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, CQuestion, NCQuestion , Response, ClubMember, MemberFeedback, Result
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
import csv, uuid
# Create your views here.
def index(request):
    result = False
    if Result.objects.filter(result_declared=True).first() is not None:
        result = True
    return render(request, 'base/index2.html', { 'result': result })

@login_required
def roundOne(request):
    user= request.user
    if request.method == 'POST':
        messages.error(request,"Registrations closed! Try contacting an EDC memeber if you still want in!")
        return redirect('/')
    #     name = request.POST['name']
    #     place = request.POST['place']
    #     branch = request.POST['branch']
    #     roll_number = request.POST['roll_number']
    #     phone_number = request.POST['phone_number']
    #     year = request.POST['year']
    #     stage = '0'
    #     if Student.objects.filter(user=user).first() is not None:
    #         s = Student.objects.get(user=user)
    #         s.user = user
    #         s.name = name
    #         s.place = place
    #         s.year = year
    #         s.branch = branch
    #         s.roll_number = roll_number
    #         s.phone_number = phone_number
    #         s.stage = '0'
    #         s.save(update_fields=['name', 'place', 'year', 'branch', 'roll_number', 'phone_number'])
    #     else:    
    #         student = Student.objects.create( user=user,name=name, year=year, stage=stage, branch=branch, place=place, roll_number=roll_number, phone_number=phone_number)
    #         student.save()
    #     messages.success(request, "Data saved successfully")
    #     return redirect('/round-1#survey-form-core')

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
        if Student.objects.filter(user=user).all().count() == 0:
            messages.error(request, 'Please fill your details first')
            return redirect('/round-1')
        student = Student.objects.filter(user=user)
        member = student.first()
        phone_number = member.phone_number
        name = member.name
        category = request.POST['category']
        Cquestions= CQuestion.objects.filter(category=category).all()
        NCquestions = NCQuestion.objects.all()
        Response.objects.filter(student=member, category=category).all().delete()
        for i in range(1,len(Cquestions)+1):
            response= "response"+str(i)
            if response in request.POST:
                ans = request.POST[response]
                Response.objects.create(student = student[0], question_text = Cquestions[i-1].question_text, question_response = ans, student_phone_number= phone_number, student_name = name, category=category)
                
            else:
                pass
        
        messages.success(request, 'Data saved successfully')
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
    if Result.objects.filter(result_declared=True).first() is not None:
        students = Student.objects.all()
        max_round = 0
        data = []
        for student in students:
            if max_round < int(student.stage):
                max_round = int(student.stage)
        for student in students:
            student_responses = Response.objects.filter(student=student)
            domain = set()
            for student_response in student_responses:
                domain.add(student_response.category)
            da = "Core, "
            for d in domain:
                if d != 'Core':
                    da = da + d + ", "
            if int(student.stage) == max_round:
                data.append({
                    'name': student.name,
                    'domain': da[0:len(da) - 2]
                })
        return render(request, 'base/results2.html', { 'data': data })
    else:
        return redirect('/')

def members(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        user = request.POST['user']
        member_feedback = MemberFeedback(member=ClubMember.objects.filter(user=request.user).first(), student=Student.objects.filter(user=User.objects.filter(username=user).first()).first())
        member_feedback.feedback = feedback
        member_feedback.save()
        return redirect(request.META.get('HTTP_REFERER'))
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
        print(request.POST)
        student = Student.objects.filter(user=User.objects.filter(username=request.POST['user']).first()).first()
        student.stage = request.POST['stage']
        student.save()
        return redirect(request.META.get('HTTP_REFERER'))

def nextRoundCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        new_students = []
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_students.append(student)
        students = new_students
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

def allUserExceptStudentsCSV(request):
    if request.user.username == 'admin':
        users = User.objects.all()
        new_users = []
        for user in users:
            if(Student.objects.all().filter(user=user).first()==None):
                if(ClubMember.objects.all().filter(user=user).first()==None):
                    new_users.append(user)
        # print(new_users)
        # students = Student.objects.all()
        # new_students = []
        # students = new_students
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students-not-registered.csv"'
        writer = csv.writer(response)
        writer.writerow(
                [
                    "Name",
                    "Email"
                ]
            )
        for user in new_users:
            writer.writerow(
                [
                    user.first_name + " " + user.last_name,
                    user.email
                ]
            )
        return response
    else:
        return redirect('/')

def allStudentsCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        new_students = []
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_students.append(student)
        students = new_students
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

def techStudentsCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        new_students = []
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_students.append(student)
        students = new_students
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="tech-students.csv"'
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
            for d in domain:
                if d =='GD'or d=='Video': 
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
    
def webStudentsCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        new_students = []
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_students.append(student)
        students = new_students
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="web-students.csv"'
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
            for d in domain:
                if d =='Web': 
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
        new_students = []
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_students.append(student)
        students = new_students
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="responses.csv"'
        writer = csv.writer(response)
        writer.writerow(
                [
                    "Name",
                    "Phone Number",
                    "Roll No.",
                    "Department",
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
                    student.phone_number,
                    student.roll_number,
                    student.branch,
                ]
            )
            for student_response in student_responses:
                writer.writerow(
                    [
                        "",
                        "",
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

def rejectedStudentsCSV(request):
    if request.user.username == 'admin':
        students = Student.objects.all()
        new_students = []
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_students.append(student)
        students = new_students
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="rejected.csv"'
        writer = csv.writer(response)
        max_round = 0
        for student in students:
            if max_round < int(student.stage):
                max_round = int(student.stage)
        writer.writerow(
                [
                    "Name",
                    "Phone Number",
                    "Round"
                ]
            )
        for student in students:
            if int(student.stage) != max_round:
                writer.writerow(
                [
                    student.name,
                    student.phone_number,
                    student.stage
                ]
            )
        return response
    else:
        return redirect('/')

def getDomains(student):
    students_responses = Response.objects.filter(student=student)
    # print(students_responses)
    domains = set()
    for response in students_responses:
        domains.add(response.category)
    domains_str = ""
    for domain in domains:
        domains_str += domain + ", "
    # print(domains_str)
    return domains_str

def allStudents(request):
    if request.user.is_authenticated and ClubMember.objects.filter(user=request.user).first() is not None:
        students = Student.objects.all()
        new_students = []
        context = []
        reviewed = ''
        for student in students:
            if ClubMember.objects.filter(user=student.user).first() is None:
                new_student = {}
                new_student['domains'] = getDomains(student)
                new_student['id'] = student.id
                new_student['name']=student.name
                new_student['branch']=student.branch
                new_student['roll_number'] = student.roll_number
                new_student['year'] = student.year
                new_student['user'] = student.user
                new_student['phone_number'] = student.phone_number
                new_student['stage'] = student.stage
                
                # new_student['']
                # print(new_student)
                # print(student)
                count = MemberFeedback.objects.filter(student=student).all().count()
                # print(count==0)
                if count == 0:
                    new_student['reviewed'] = 'No'
                else:
                    new_student['reviewed'] = 'Yes'
                new_students.append(new_student)
                context.append({
                    'student': new_student
                })
        # print(context)
        return render(request, 'base/table-admin2.html', { 'data': context  })
    else:
        return redirect('/')

def studentId(request, slug):
    if request.user.is_authenticated and ClubMember.objects.filter(user=request.user).first() is not None:
        student = Student.objects.get(id=slug)
        data = []
        responses = Response.objects.filter(student=student).all()
        all_feedback = MemberFeedback.objects.filter(student=student).all()
        member_feedback = MemberFeedback.objects.filter(student=student, member=ClubMember.objects.filter(user=request.user).first()).first()
        domains = getDomains(student)
        data.append({
            'student': student,
            'domains': domains,
            'responses': responses,
            'all_feedback': all_feedback,
            'member_feedback': member_feedback
        })
        return render(request, 'base/profile2.html', { 'data': data })
    else:
        return redirect('/')