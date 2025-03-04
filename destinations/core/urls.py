from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/new/", views.new_user, name="new_user"),
    path("users/", views.create_user, name="create_user"),
    path("sessions/new/", views.login, name="login"),
    path("sessions/", views.authenticate, name="authenticate"),
    path("sessions/destroy/", views.logout, name="logout"),
]
