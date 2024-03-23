from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate , login
# Create your views here.


class SignupStudent(CreateView):
    model = User
    form_class = SignupStudent
    template_name = 'signupstudent.html'


    def form_valid(self,form):
        user = form.save()
        return redirect('homepage')
class SignupLecturer(CreateView):
    model = User
    form_class = SignupLecturer
    template_name = 'signuplecturer.html'


    def form_valid(self,form):
        user = form.save()
        return redirect('homepage')
class SignupParent(CreateView):
        model = User
        form_class = SignupParent
        template_name = 'signupparent.html'

        def form_valid(self, form):
            user = form.save()
            return redirect('homepage')


def loginstudent(request):
    if request.method == "GET" :
        return render(request,'loginstudent.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('modelstudent')
        else:
            print("Make sure that your Username and password are correct")
            return redirect('loginstudent')



def loginadmin(request):
    if request.method == "GET" :
        return render(request,'loginadmin.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            print("Make sure that your Username and password are correct")
            return redirect('loginadmin')


def loginparent(request):
    if request.method == "GET" :
        return render(request,'loginparent.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('homepage')
        else:
            print("Make sure that your Username and password are correct")

            return redirect('loginparent')

def loginlecturer(request):
    if request.method == "GET" :
        return render(request,'loginlecturer.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('modellecturer')
        else:
            print("Make sure that your Username and password are correct")
            return redirect('loginlecturer')


def modelstudent(request):
     return render(request,'modelstudent.html')


def modellecturer(request):
    return render(request, 'modellecturer.html')

def homepage(request):
    return render(request , 'homepage.html')