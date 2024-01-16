import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth.models import User
from markdown2 import Markdown

from .models import Course, User, Module

def index(request):
    return render(request, "Bridge/index.html")

@csrf_exempt
@login_required
def classes(request):

    user = request.user

    courses = Course.objects.filter(Q(teacher=user) | Q(students=user))

    return render(request, "Bridge/classes.html", {'classes': courses})


def register_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]

        password = request.POST["password"]
        confirmation = request.POST["password-confirmation"]
        if password != confirmation:
            return render(request, "Bridge/index.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "Bridge/index.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("classes"))
    else:
        return render(request, "Bridge/index.html")
    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("classes"))
        else:
            return render(request, "Bridge/index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Bridge/index.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@require_GET
def check_login_status(request):
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'is_authenticated': is_authenticated})

@csrf_exempt
@login_required
def new_class(request):
    if request.method == "POST":
        name = request.POST["class_name"]
        location = request.POST["location"]
        image = request.POST["backgroundImage"]
        teacher = request.user

        if not name or not location:
            return render(request, "Bridge/classes.html", {
                "message": "Name or location cannot be empty."
            })

        new_class = Course.objects.create(
            class_name=name,
            location=location,
            class_picture=image,
            teacher=teacher,
        )

        new_class.save()
        
        return HttpResponseRedirect(reverse("classes"))
    else:
        return render(request, "Bridge/classes.html")
    
@csrf_exempt
@login_required
def view_class(request, class_id):

    course_instance = get_object_or_404(Course, id=class_id)
    modules = course_instance.modules.all()

    return render(request, "Bridge/class.html", {
        'class_id': class_id,
        'course': course_instance,
        'modules': modules
    })


@csrf_exempt
@login_required
def view_module(request, moduele_id, class_id):

    course_instance = get_object_or_404(Course, id=class_id)
    module_instance = Module.objects.filter(Q(id=moduele_id))

    module_title = module_instance.title
    module_description = module_instance.description
    module_content = module_instance.content

    markdown = Markdown()

    description = markdown.convert(module_description)
    content = markdown.convert(module_content)

    return render(request, "Bridge/view_module.html", {
        "class": course_instance,
        "title": module_title,
        "description": description,
        "content": content
    })

@csrf_exempt
@login_required
def add_module(request, class_id):

    course_instance = get_object_or_404(Course, id=class_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')


        new_module = Module.objects.create(title=title, description=description, content=content)
        course_instance.modules.add(new_module) 
        course_instance.save()

        return HttpResponseRedirect(reverse("view_class", args=[class_id]))

    return render(request, 'Bridge/add_module.html', {
        "class": course_instance
    })

@csrf_exempt
@login_required
def add_student(request, class_id):

    course_instance = get_object_or_404(Course, id=class_id)

    if request.method == 'POST':
        if request.method == 'POST':
            
            username = request.POST.get('student_username')

            try:
                student = User.objects.get(username=username)

            except User.DoesNotExist:
                return render(request, 'Bridge/class.html', {
                    "course": course_instance,
                    "message": "Student with the provided ID does not exist."
                })

        # Add the student to the course
        course_instance.students.add(student)

    return render(request, 'Bridge/add_student.html', {
        "class": course_instance
    })

def student_form(request, class_id):

    course_instance = get_object_or_404(Course, id=class_id)


    return render(request, 'Bridge/add_student.html', {
                    "course": course_instance,
                    "class": course_instance
                })
