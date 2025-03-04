from django.shortcuts import render
from models import Destination
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseBadRequest


def index(request: HttpRequest):
    destinations = Destination.objects.filter(share_publicly=True).order_by('-id')[:5]
    return render(request, "core/index.html", {"destinations": destinations})


