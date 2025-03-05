from django.http import HttpRequest, HttpResponseRedirect
from .models import Session


def session_middleware(next):
    def middleware(request: HttpRequest):
        # Check if session token exists and if login required
        if "session_token" not in request.COOKIES or not Session.objects.filter(token=request.COOKIES["session_token"]).exists():
            # Redirect to login page if not logged in
            if request.path.startswith("/destinations/") or request.path == "/sessions/destroy/":
                return HttpResponseRedirect("/sessions/new/")
            res = next(request)
            return res
        # Set request.user to the logged-in user
        token = request.COOKIES.get("session_token")
        user = Session.objects.filter(token=token).first().user
        request.user = user
        res = next(request)
        return res
    return middleware


def not_found_middleware(next):
    def middleware(request: HttpRequest):
        res = next(request)
        # Redirect to 404 page if page not found
        if res.status_code == 404:
            return HttpResponseRedirect("/404/")
        return res
    return middleware
