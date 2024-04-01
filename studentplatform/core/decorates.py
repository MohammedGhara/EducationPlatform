from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse

def limit_to_student(view_func):

    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='student').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper

def limit_to_parent(view_func):

    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='parent').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper

def limit_to_lecturer(view_func):

    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='lecturer').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper

def limit_to_admin(view_func):

    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized to access this page.")
    return wrapper
