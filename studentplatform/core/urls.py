from django.contrib import admin
from django.urls import path ,include
from .views import *
from . import views
import os
urlpatterns = [
    path('', homepage, name='homepage'),
    path('signupstudent/',SignupStudent.as_view()  , name='signupstudent'),
    path('signupparent/',SignupParent.as_view() , name='signupparent'),
    path('signuplecturer/', SignupLecturer.as_view(), name='signuplecturer'),
    path('loginstudent/',loginstudent, name='loginstudent'),
    path('logout/',logout_user, name='logout'),
    path('loginadmin/',loginadmin, name='loginadmin'),
    path('loginparent/',loginparent, name='loginparent'),
    path('loginlecturer/',loginlecturer, name='loginlecturer'),
    path('modelstudent/', modelstudent, name='modelstudent'),
    path('modellecturer/', modellecturer, name='modellecturer'),
    path('adminpage/',adminpage, name='adminpage'),
    path('modelparent/', modelparent, name='modelparent'),
    path('class10/', class10, name='class10'),
    path('class11/', class11, name='class11'),
    path('class12/', class12, name='class12'),
    path('index/',views.index, name='index'),
    path('download/', download_file, name='download'),
    path('algebrastudent/', algebrastudent, name='algebrastudent'),
    path('calculusstudent/', calculusstudent, name='calculusstudent'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('aad/', views.home, name='home'),
    path('se', views.getMessages, name='getMessages'),
    path('search',views.search,name='search'),



]