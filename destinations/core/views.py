from django.shortcuts import render
from .models import Destination, User, Session
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
        return HttpResponseBadRequest("All fields must be filled <br> <a href='/users/new/'>Go back</a>")
    if User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("Email already exists <br> <a href='/users/new/'>Go back</a>")
    if email.count("@") != 1 or email.count(".") == 0:
        return HttpResponseBadRequest("Invalid email <br> <a href='/users/new/'>Go back</a>")
    if len(password) < 8:
        return HttpResponseBadRequest("Password must be at least 8 characters <br> <a href='/users/new/'>Go back</a>")

    # Create user
    user = User(name=name, email=email, password_hash=make_password(password))
    user.save()
    session = Session(user=user, token=make_password(email))
    session.save()
    res = HttpResponseRedirect("/")
    res.set_cookie("session_token", session.token)
    return res


def login(request: HttpRequest):
    return render(request, "core/login.html")


def authenticate(request: HttpRequest):
    email = request.POST["email"]
    password = request.POST["password"]
    if not User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("Email does not exist <br> <a href='/login/'>Go back</a>")
    user = User.objects.get(email=email)
    if not check_password(password, user.password_hash):
        return HttpResponseBadRequest("Incorrect password <br> <a href='/login/'>Go back</a>")
    session = Session(user=user, token=make_password(email))
    session.save()
    res = HttpResponseRedirect("/")
    res.set_cookie("session_token", session.token)
    return res


def logout(request: HttpRequest):
    session = Session.objects.get(token=request.COOKIES["session_token"])
    session.delete()
    res = HttpResponseRedirect("/")
    res.delete_cookie("session_token")
    return res

