from django.http import HttpRequest, HttpResponseRedirect
from .models import Session

def session_middleware(next):
    def middleware(request: HttpRequest):

        if "session_token" not in request.COOKIES or not Session.objects.filter(token=request.COOKIES["session_token"]).exists():
            if request.path.startswith("/destinations/") or request.path == "/sessions/destroy/":
                return HttpResponseRedirect("/sessions/new/")
            res = next(request)
            return res
        token = request.COOKIES.get("session_token")
        user = Session.objects.filter(token=token).first().user
        request.user = user
        res = next(request)
        return res
    return middleware


def not_found_middleware(next):
    def middleware(request: HttpRequest):
        res = next(request)
        if res.status_code == 404:
            return HttpResponseRedirect("/404/")
        return res
    return middleware
