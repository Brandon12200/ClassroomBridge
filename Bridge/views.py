import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from markdown2 import Markdown

from .models import Course, User, Module
from .forms import RegisterForm, LoginForm, NewClassForm, AddModuleForm, AddStudentForm, EditHomepageForm


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
        confirmation = request.POST["password-confirmation"]  # Keep hyphenated name to match template
        if password != confirmation:
            return render(request, "Bridge/index.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError as e:
            print(e)
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, "Bridge/index.html", {
                    "message": "Username already taken."
                })
            # Check if email already exists
            elif User.objects.filter(email=email).exists():
                return render(request, "Bridge/index.html", {
                    "message": "Email address already taken."
                })
            else:
                return render(request, "Bridge/index.html", {
                    "message": "Registration failed. Please try again with different credentials."
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
        form = NewClassForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["class_name"]
            location = form.cleaned_data["location"]
            image = form.cleaned_data.get("class_picture")  # Get the uploaded image file
            teacher = request.user

            new_class = Course.objects.create(
                class_name=name,
                location=location,
                teacher=teacher,
            )
            
            # Handle the image file if it exists
            if image:
                new_class.class_picture = image
                new_class.save()

            return HttpResponseRedirect(reverse("classes"))
        else:
            return render(request, "Bridge/classes.html", {
                "message": "Form invalid. Please check your input."
            })
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
    modules = course_instance.modules.all().order_by('order', 'created_at')

    # Check if user is the teacher or a student in this class
    is_teacher = request.user == course_instance.teacher
    is_student = request.user in course_instance.students.all()
    
    if not (is_teacher or is_student):
        return HttpResponseRedirect(reverse("classes"))

    if course_instance.home_content is not None:
        markdown = Markdown()
        content = markdown.convert(course_instance.home_content)
    else:
        content = "No content available"

    # Count students for display
    student_count = course_instance.students.count()

    return render(request, "Bridge/class.html", {
        'class_id': class_id,
        'course': course_instance,
        'modules': modules,
        'content': content,
        'is_teacher': is_teacher,
        'student_count': student_count
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
    
    # Check if user is the teacher or a student in this class
    is_teacher = request.user == course_instance.teacher
    is_student = request.user in course_instance.students.all()
    
    if not (is_teacher or is_student):
        return HttpResponseRedirect(reverse("classes"))
    
    # Check if module belongs to this class
    if module_instance not in course_instance.modules.all():
        return HttpResponseRedirect(reverse("view_class", args=[class_id]))

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
    
    # Only the teacher can add modules
    if request.user != course_instance.teacher:
        return HttpResponseRedirect(reverse("view_class", args=[class_id]))

    if request.method == 'POST':
        # Process direct POST data instead of using form
        title = request.POST.get('title')
        description = request.POST.get('description')
        content = request.POST.get('content')
        order = request.POST.get('order', 0)
        
        try:
            order = int(order)
        except ValueError:
            order = 0
        
        if title and description and content:
            # Create new module with order
            new_module = Module.objects.create(
                title=title, 
                description=description, 
                content=content,
                order=order
            )
            course_instance.modules.add(new_module)
            course_instance.save()

            return HttpResponseRedirect(reverse("view_class", args=[class_id]))
        else:
            return render(request, 'Bridge/add_module.html', {
                "class": course_instance,
                "message": "All fields are required."
            })

    # Get the highest order number from existing modules to suggest the next
    latest_order = course_instance.modules.aggregate(models.Max('order'))['order__max'] or 0
    next_order = latest_order + 1

    return render(request, 'Bridge/add_module.html', {
        "class": course_instance,
        "next_order": next_order
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
    """
    try:
        course_instance = get_object_or_404(Course, id=class_id)
        
        # Only the teacher can add students
        if request.user != course_instance.teacher:
            return HttpResponseRedirect(reverse("view_class", args=[class_id]))
        
        modules = course_instance.modules.all()

        if course_instance.home_content is not None:
            markdown = Markdown()
            content = markdown.convert(course_instance.home_content)
        else:
            content = "No content available"

        if request.method == 'POST':
            # Use the field name from the template
            username = request.POST.get('student_username')

            if not username:
                return render(request, 'Bridge/add_student.html', {
                    "class": course_instance,
                    "message": "Student username is required."
                })

            try:
                student = User.objects.get(username=username)
                
                # Check if student is already in the class
                if student in course_instance.students.all():
                    return render(request, 'Bridge/add_student.html', {
                        "class": course_instance,
                        "message": f"Student '{username}' is already in this class."
                    })
                
                # Don't add teachers as students
                if student.is_staff:
                    return render(request, 'Bridge/add_student.html', {
                        "class": course_instance,
                        "message": "Cannot add a teacher as a student."
                    })
                    
                course_instance.students.add(student)

                return HttpResponseRedirect(reverse("view_class", args=[class_id]))
            except User.DoesNotExist:
                return render(request, 'Bridge/add_student.html', {
                    "class": course_instance,
                    "message": f"Student with username '{username}' does not exist."
                })
            except Exception as e:
                return render(request, 'Bridge/add_student.html', {
                    "class": course_instance,
                    "message": f"An error occurred: {str(e)}"
                })

        return render(request, 'Bridge/add_student.html', {
            "class": course_instance
        })
    except Exception as e:
        return render(request, "Bridge/error.html", {
            "error_message": f"An unexpected error occurred: {str(e)}"
        })


@csrf_exempt
@login_required
def student_form(request, class_id):
    """
    Renders the add_student.html template for a specific class.
    Allows searching for students by username or email.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class.

    Returns:
        HttpResponse: The HTTP response containing the rendered template.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    
    # Only the teacher can see this form
    if request.user != course_instance.teacher:
        return HttpResponseRedirect(reverse("view_class", args=[class_id]))
    
    # Get current students for display
    current_students = course_instance.students.all().order_by('username')
    
    # Handle search functionality
    search_term = request.GET.get('search', '')
    search_results = []
    
    if search_term:
        # Search for users by username or email, excluding the teacher and current students
        search_results = User.objects.filter(
            Q(username__icontains=search_term) | Q(email__icontains=search_term)
        ).exclude(
            Q(id=request.user.id) | Q(id__in=current_students.values_list('id', flat=True))
        ).exclude(
            is_staff=True
        ).order_by('username')[:10]  # Limit to 10 results for performance
        
    return render(request, 'Bridge/add_student.html', {
        "course": course_instance,
        "class": course_instance,
        "current_students": current_students,
        "search_term": search_term,
        "search_results": search_results
    })


@csrf_exempt
@login_required
def remove_student(request, class_id, student_id):
    """
    Removes a student from a class.

    Args:
        request (HttpRequest): The HTTP request object.
        class_id (int): The ID of the class.
        student_id (int): The ID of the student to remove.

    Returns:
        HttpResponse: Redirect to the student form page.
    """
    course_instance = get_object_or_404(Course, id=class_id)
    
    # Only the teacher can remove students
    if request.user != course_instance.teacher:
        return HttpResponseRedirect(reverse("view_class", args=[class_id]))
    
    try:
        student = User.objects.get(id=student_id)
        if student in course_instance.students.all():
            course_instance.students.remove(student)
            return HttpResponseRedirect(reverse("student_form", args=[class_id]))
        else:
            return render(request, 'Bridge/add_student.html', {
                "class": course_instance,
                "message": f"Student is not enrolled in this class."
            })
    except User.DoesNotExist:
        return render(request, 'Bridge/add_student.html', {
            "class": course_instance,
            "message": f"Student with ID {student_id} does not exist."
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
    
    # Only the teacher can edit the homepage
    if request.user != course_instance.teacher:
        return HttpResponseRedirect(reverse("view_class", args=[class_id]))
        
    modules = course_instance.modules.all().order_by('order', 'created_at')
    # Count students for display in redirect
    student_count = course_instance.students.count()

    if request.method == 'POST':
        # Use the field name from the template
        home_content = request.POST.get('home-content')
        course_instance.home_content = home_content
        course_instance.save()

        # Redirect to view_class instead of rendering the template directly
        return HttpResponseRedirect(reverse("view_class", args=[class_id]))

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