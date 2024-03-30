from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate , login , logout
from .models import Room , Message , Lecturer
from django.urls import reverse
import os
from django.contrib.auth.models import Group
# Create your views here.
from .decorates import *
class SignupStudent(CreateView):
    model = User
    form_class = SignupStudent
    template_name = 'signupstudent.html'

    def form_valid(self, form):
        user = form.save()
        student_group = Group.objects.get(name='student')
        student_group.user_set.add(user)
        return redirect('homepage')

class SignupAdmin(CreateView):
    model = User
    form_class = Signupadmin
    template_name = 'signupadmin.html'

    def form_valid(self, form):
        user = form.save()
        return redirect('homepage')

class SignupLecturer(CreateView):
    model = User
    form_class = SignupLecturer
    template_name = 'signuplecturer.html'

    def form_valid(self, form):
        user = form.save()
        lecturer_group = Group.objects.get(name='lecturer')
        lecturer_group.user_set.add(user)
        return redirect('homepage')

class SignupParent(CreateView):
    model = User
    form_class = SignupParent
    template_name = 'signupparent.html'

    def form_valid(self, form):
        user = form.save()
        parent_group = Group.objects.get(name='parent')
        parent_group.user_set.add(user)
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
    if request.method == "GET":
        return render(request, 'loginadmin.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/admin/')
        else:
            print("Make sure that your Username and password are correct")
            return redirect('loginadmin')
def loginparent(request):
    if request.method == "GET":
        return render(request, 'loginparent.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('modelparent')
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

def logout_user(request):
    logout(request)
    return redirect('homepage')


def class10(request):
    return render(request,'class10.html')
def class11(request):
    return render(request,'class11.html')
def class12(request):
    return render(request,'class12.html')

@login_required
@limit_to_student
def modelstudent(request):
    return render(request,'modelstudent.html')
@login_required
@limit_to_parent
def modelparent(request):
    return render(request, 'modelparent.html')
@login_required
@limit_to_lecturer
def modellecturer(request):
    return render(request, 'modellecturer.html')
def calculusstudent(request):
    return render(request, 'calculusstudent.html')
def algebrastudent(request):
    return render(request, 'algebrastudent.html')

def homepage(request):
    return render(request , 'homepage.html')
def home(request):
    return render(request, 'home.html')
@login_required
@limit_to_admin
def adminpage(request):
    return render(request, 'adminpage.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

def search(request):
    query = request.GET.get('query', '').strip().lower()
    if not query:
        # No search query was entered
        return HttpResponse("You did not search for anything.")

    # Define a mapping of keywords to view names (URL names)
    search_mappings = {
        'student': 'modelstudent',
        'Courses Student': 'modelstudent',
        'lecturer': 'modellecturer',
        ' Courses lecturer': 'modellecturer',
        'LecturerClasses': 'modellecturer',
        'calculs for lecturer': 'modellecturer',
        'Linear Algebra for lecturer': 'modellecturer',
        'parent': 'modelparent',
        'Child Class': 'modelparent',
        'כיתה י': 'modelparent',
        'כיתה יא': 'modelparent',
        'כיתה יב': 'modelparent',
    }


    for keyword, view_name in search_mappings.items():
        if query == keyword:

            return redirect(reverse(view_name))


    return HttpResponse(f"No results found for '{query}'.")


from django.http import HttpResponse
from django.shortcuts import render
from .forms import LecturerForm
from .models import Lecturer
import os


def index(request):
    if request.method == "POST":
        form = LecturerForm(request.POST, request.FILES)
        if form.is_valid():
            lecturer = form.save()
            return redirect('index')
    else:
        form = LecturerForm()

    lecturer = Lecturer.objects.last()
    file_path = None

    if lecturer and lecturer.file:
        file_path = lecturer.file.path

    if file_path and os.path.exists(file_path):
        file_url = lecturer.file.url
    else:
        file_url = None

    return render(request, 'index.html', {'form': form, 'file_url': file_url})



