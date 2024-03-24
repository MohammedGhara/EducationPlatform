from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate , login , logout
from .models import Room , Message


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

def logout_user(request):
    logout(request)
    return redirect('homepage')



def modelstudent(request):
    return render(request,'modelstudent.html')


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
