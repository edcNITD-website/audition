from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from base.models import *

# Create your views here.


def memberlogin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user_obj = authenticate(request, username=username, password=password)

        if user_obj is None:
            return render(request, 'members/login.html')
        elif user_obj.is_superuser:
            login(request, user_obj)
            return redirect(reverse('dashboard'))
    return render(request, 'members/login.html')


def dashboard(request):
    if not request.user.is_superuser:
        return HttpResponse("permisson denied")
    return render(request,'members/dashboard.html')


def students(request):
    pass


def questions(request):
    id = None
    item = None
    show = request.GET.get('show', "")
    if show == "edit":
        id = request.GET.get('id')
        item = CQuestion.objects.get(id=id)
    if show == "delete":
        id = request.GET.get('id')
        item = CQuestion.objects.get(id=id)
    objs = CQuestion.objects.all()
    core = objs.filter(category="o")
    web = objs.filter(category="w")
    gd = objs.filter(category="g")
    video = objs.filter(category="v")
    content = objs.filter(category="c")
    context = {'core': core,
               'web': web,
               'gd': gd,
               'video': video,
               'content': content,
               'show': show,
               'item': item}

    return render(request, 'members/questions.html', context)


def add(request):
    if request.method == 'POST':
        category = request.POST.get("category")
        type = request.POST.get("type")
        question_text = request.POST.get("question")
        question = CQuestion(
            question_text=question_text,
            type=type,
            category=category
        )
        question.save()
        return redirect('/members/questions/')
    return redirect('/members/questions/?show=add')


def edit(request, id):
    if request.method == 'POST':
        category = request.POST.get("category")
        type = request.POST.get("type")
        question_text = request.POST.get("question")
        update = CQuestion.objects.get(id=id)
        update.question_text = question_text
        update.type = type
        update.category = category
        update.save()
        return redirect(reverse('member_questions'))
    return redirect(reverse('member_questions') + '?show=edit&id=' + str(id))


def delete(request,id):
    if request.method == 'POST':
        remove = CQuestion.objects.get(id=id)
        remove.delete()
        return redirect(reverse('member_questions'))
    return redirect(reverse('member_questions') + '?show=delete&id=' + str(id))
    pass
