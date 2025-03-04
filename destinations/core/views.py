from django.shortcuts import render
from .models import Destination, User
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.hashers import make_password, check_password


def index(request: HttpRequest):
    destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    return render(request, "core/index.html", {"destinations": destinations})


def new_user(request: HttpRequest):
    return render(request, "core/new_user.html")


def create_user(request :HttpRequest):
    # Validation
    name = request.POST["name"]
    email = request.POST["email"]
    password = request.POST["password"]
    if name == "" or email == "" or password == "":
        return HttpResponseBadRequest("All fields must be filled <br> <a href='/new_user/'>Go back</a>")
    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("Email already exists <br> <a href='/new_user/'>Go back</a>")

    # Create user
    user = User(name=name, email=email, password_hash=make_password(password))
    user.save()
    return HttpResponseRedirect("/")