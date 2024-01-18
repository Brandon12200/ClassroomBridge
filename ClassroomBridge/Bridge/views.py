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
    """
    Renders the index.html template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    return render(request, "Bridge/index.html")


@csrf_exempt
@login_required
def classes(request):
    """
    Renders the classes.html template with the list of courses.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """

    user = request.user

    courses = Course.objects.filter(Q(teacher=user) | Q(students=user))

    return render(request, "Bridge/classes.html", {'classes': courses})


def register_view(request):
    """
    Handles the registration of a new user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
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
    """
    Handles the login of a user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
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
    """
    Logs out the current user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@require_GET
def check_login_status(request):
    """
    Checks if the user is authenticated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response containing the login status.
    """
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'is_authenticated': is_authenticated})


@csrf_exempt
@login_required
def new_class(request):
    """
    Handles the creation of a new class.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
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
    """
    Renders the class.html template with the details of a specific class.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class to view.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    modules = course_instance.modules.all()

    if course_instance.home_content is not None:
        markdown = Markdown()
        content = markdown.convert(course_instance.home_content)
    else:
        content = "No content available"

    return render(request, "Bridge/class.html", {
        'class_id': class_id,
        'course': course_instance,
        'modules': modules,
        'content': content
    })


@csrf_exempt
@login_required
def view_module(request, module_id, class_id):
    """
    Renders the view_module.html template with the details of a specific module.

    Args:
        request (HttpRequest): The HTTP request object.
        module_id (int): The ID of the module to view.
        class_id (int): The ID of the class that the module belongs to.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    module_instance = get_object_or_404(Module, id=module_id)

    module_title = module_instance.title
    module_description = module_instance.description
    module_content = module_instance.content

    markdown = Markdown()

    if module_description is not None:
        description = markdown.convert(module_description)
    else:
        description = "No description available"

    if module_content is not None:
        content = markdown.convert(module_content)
    else:
        content = "No content available"

    return render(request, "Bridge/view_module.html", {
        "class": course_instance,
        "title": module_title,
        "description": description,
        "content": content
    })


@csrf_exempt
@login_required
def add_module(request, class_id):
    """
    Handles the creation of a new module for a class.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class to add the module to.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
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
    """
    Adds a student to a class.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class to add the student to.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.

    Raises:
        Http404: If the specified class does not exist.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    modules = course_instance.modules.all()

    if course_instance.home_content is not None:
        markdown = Markdown()
        content = markdown.convert(course_instance.home_content)
    else:
        content = "No content available"

    if request.method == 'POST':
        username = request.POST.get('student_username')

        try:
            student = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'Bridge/class.html', {
                "course": course_instance,
                "message": "Student with the provided ID does not exist.",
                "content": content,
                "modules": modules
            })

        course_instance.students.add(student)

        return render(request, 'Bridge/class.html', {
            "course": course_instance,
            "message": "Added " + username + " to the class.",
            "content": content,
            "modules": modules
        })

    return render(request, 'Bridge/add_student.html', {
        "class": course_instance,
        "content": content
    })


@csrf_exempt
@login_required
def student_form(request, class_id):
    """
    Renders the add_student.html template for a specific class.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    return render(request, 'Bridge/add_student.html', {
        "course": course_instance,
        "class": course_instance
    })


@csrf_exempt
@login_required
def edit_class_homepage(request, class_id):
    """
    Handles the editing of the homepage content for a class.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    modules = course_instance.modules.all()

    if request.method == 'POST':
        home_content = request.POST.get('home-content')
        course_instance.home_content = home_content
        course_instance.save()

        if course_instance.home_content is not None:
            markdown = Markdown()
            content = markdown.convert(course_instance.home_content)
        else:
            content = "No content available"

        return render(request, 'Bridge/class.html', {
            "course": course_instance,
            "content": content,
            "modules": modules
        })

    if course_instance.home_content is not None:
        markdown = Markdown()
        content = markdown.convert(course_instance.home_content)
    else:
        content = "No content available"
    return render(request, 'Bridge/edit_class_homepage.html', {
        "course": course_instance,
        "content": content,
        "modules": modules
    })

