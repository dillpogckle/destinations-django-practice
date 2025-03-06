from django.shortcuts import render
from .models import Destination, User, Session
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.hashers import make_password, check_password
import secrets


def index(request: HttpRequest):
    # Check if user is logged in and render home page
    is_logged_in = "session_token" in request.COOKIES and Session.objects.filter(token=request.COOKIES["session_token"]).exists()
    destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    return render(request, "core/index.html", {"destinations": destinations, "is_logged_in": is_logged_in})


def new_user(request: HttpRequest):
    # Render new user page
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
    if not any(char.isdigit() for char in password):
        return HttpResponseBadRequest("Password must contain at least one number <br> <a href='/users/new/'>Go back</a>")

    # Create user
    user = User(name=name, email=email, password_hash=make_password(password))
    user.save()
    session = Session(user=user, token=secrets.token_hex(32))
    session.save()
    res = HttpResponseRedirect("/")
    res.set_cookie("session_token", session.token)
    return res


def login(request: HttpRequest):
    # Render login page
    return render(request, "core/login.html")


def authenticate(request: HttpRequest):
    # Validation
    email = request.POST["email"]
    password = request.POST["password"]
    if not User.objects.filter(email=email).exists():
        return HttpResponseBadRequest("Email does not exist <br>  <a href='/users/new/'>Create an Account</a>")
    user = User.objects.get(email=email)
    if not check_password(password, user.password_hash):
        return HttpResponseBadRequest("Incorrect password <br> <a href='/sessions/new/'>Try Again</a>")
    session = Session(user=user, token=secrets.token_hex(32))
    session.save()
    res = HttpResponseRedirect("/")
    res.set_cookie("session_token", session.token)
    return res


def logout(request: HttpRequest):
    # Delete session and redirect to home page
    session = Session.objects.get(token=request.COOKIES.get("session_token"))
    session.delete()
    res = HttpResponseRedirect("/")
    res.delete_cookie("session_token")
    return res


def destinations(request: HttpRequest):
    # Create destination
    if request.method == "POST":
        user = request.user
        name = request.POST["name"]
        review = request.POST["review"]
        rating = request.POST["rating"]
        share_publicly = request.POST.get("share_publicly", False)
        if share_publicly == "on":
            share_publicly = True
        else:
            share_publicly = False
        destination = Destination(name=name, review=review, rating=rating, user=user, share_publicly=share_publicly)
        destination.save()
        return HttpResponseRedirect("/destinations/")

    # Render destinations page
    user = request.user
    destinations = Destination.objects.filter(user=user)
    return render(request, "core/destinations.html", {"destinations": destinations})


def new_destination(request: HttpRequest):
    # Render new destination page
    return render(request, "core/new_destination.html")


def destination(request: HttpRequest, id: int):
    # Update destination
    if request.method == "POST":
        destination = Destination.objects.get(id=id)
        destination.name = request.POST["name"]
        destination.review = request.POST["review"]
        destination.rating = request.POST["rating"]
        share_publicly = request.POST.get("share_publicly", False)
        if share_publicly == "on":
            share_publicly = True
        else:
            share_publicly = False
        destination.share_publicly = share_publicly
        destination.save()
        return HttpResponseRedirect("/destinations/")

    # Render destination page
    destination = Destination.objects.get(id=id)
    if destination.user != request.user:
        return HttpResponseRedirect("/404/")
    return render(request, "core/destination.html", {"destination": destination})


def delete_destination(request: HttpRequest, id: int):
    # Delete destination and redirect to destinations page
    Destination.objects.get(id=id).delete()
    return HttpResponseRedirect("/destinations/")


def not_found(request: HttpRequest):
    # 404 page
    return render(request, "core/404.html")
