"""
URL configuration for resumescreener project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('resume_screener/templates/aboutus.html',views.aboutus,name='aboutus'),
    path('resume_screener/templates/careeradvice.html',views.careeradvice,name='careeradvice'),
    path('resume_screener/templates/contact.html',views.contact,name='contact'),
    path('resume_screener/templates/Employeesignup.html',views.employeesignup,name='Employeesignup'),
    path('resume_screener/templates/Employersignup.html',views.employersignup,name='Employersignup'),
    path('resume_screener/templates/loginpage.html',views.Login,name='Login'),
    path('loginaction/',views.loginaction,name='loginaction'),
    path('resume_screener/templates/singlepost.html',views.singlepost,name='singlepost'),
    path('resume_screener/templates/search.html',views.search,name='search'),
    path('resume_screener/templates/demo.html',views.search,name='demo'),
    path('resume_screener/templates/employeeloginpage.html',views.employeeloginpage,name='employeeloginpage'),
    path('employeeloginaction/',views.employeeloginaction,name='employeeloginaction'),
    path('employeepage/', views.employeepage, name='employeepage'),
    path('pdf/<str:file_path>/', views.pdf_view, name='pdf_view'),


    
    
    
]
