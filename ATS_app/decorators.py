from functools import wraps
from django.http import HttpResponseForbidden

def recruiter_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 1:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied")
    return wrap

def candidate_required(function):
    @wraps(function) 
    def wrap(request, *args, **kwargs):
        if request.user.user_type == 2:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page")
    return wrap
