from django.contrib import admin
from django.urls import path ,include
from .views import *
from . import views

urlpatterns = [
    path('home', home, name='home'),
    path('', homepage, name='homepage'),
    path('signupstudent/',SignupStudent.as_view() , name='signupstudent'),
    path('signupparent/',SignupParent.as_view() , name='signupparent'),
    path('signuplecturer/',SignupLecturer.as_view() , name='signupLecturer'),
    path('loginstudent/',loginstudent, name='loginstudent'),
    path('logout/',logout_user, name='logout'),
    path('loginparent/',loginparent, name='loginparent'),
    path('loginlecturer/',loginlecturer, name='loginlecturer'),
    path('modelstudent/', modelstudent, name='modelstudent'),
    path('modellecturer/', modellecturer, name='modellecturer'),
    path('<str:room>/', views.room,name='room'),
    path('checkview', views.checkview,name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),




]