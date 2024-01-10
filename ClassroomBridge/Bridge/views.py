import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from .models import User

def index(request):
    return render(request, "Bridge/index.html")

@csrf_exempt
@login_required
def classes(request):
    return render(request, "Bridge/classes.html")


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        first = request.POST["first-name"]
        last = request.POST["last-name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["password-confirmation"]
        if password != confirmation:
            return render(request, "Bridge/index.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(first, last, email, password)
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
    

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("classes"))
        else:
            return render(request, "Bridge/index.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "Bridge/index.html")


def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@require_GET
def check_login_status(request):
    return JsonResponse({'is_authenticated': False})