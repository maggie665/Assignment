"""Assignment1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from Attendance_System.views import RegistrationView, CustomRegistration, file_upload, sendEmail
from django.contrib import admin
from django.urls import path, include
# from Attendance_System.models import Class, Course, CollegeDay, Lecturer, Student, Semester
from  Attendance_System import views, account
from django.apps import apps
from django.conf import settings


urlpatterns = [
    # path("", index, name='home'),
    path("admin/", admin.site.urls),
    path("", views.login,name="login"),
    path("login/", views.login,name="login"),
    path("logout/", views.logout,name="logout"),
    path("semester/list/",views.semester_list),
    path("semesters/add/",views.semester_add),
    path('semesters/<int:nid>/edit/', views.semester_edit),
    path('semesters/delete/', views.semester_delete),

    path("lecturer/list/",views.lecturer_list),
    path("lecturer/add/",views.lecturer_add),
    path('lecturer/<int:nid>/edit/', views.lecturer_edit),
    path('lecturer/delete/', views.lecturer_delete),


    path("student/list/",views.student_list),
    path("student/add/",views.student_add),
    path('student/<int:nid>/edit/', views.student_edit),
    path('student/delete/', views.student_delete),

    path("class/list/", views.class_list),
    path("class/add/", views.class_add),
    path('class/<int:nid>/edit/', views.class_edit),
    path('class/delete/', views.class_delete),


    path('info/list/', views.info_list),
    path('info/add/', views.info_add),
    path('info/delete/', views.info_delete),
    path('collegeday/list/', views.collegeday_list),
    path('course/list/', views.course_list),
    path('collegeday/delete/', views.collegeday_delete),
    path('collegeday/add/', views.collegeday_add),
    path('course/add/', views.course_add),
    path('course/delete/', views.course_delete),
    path('course/<int:nid>/edit/', views.course_edit),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create", RegistrationView.as_view(), name="register"),
    path("accounts/custom_create", CustomRegistration, name="custom_register"),
    path('file_upload/', file_upload, name='file-upload'),
    path('send_email/', sendEmail, name='send_email'),
    path('administrator/list/', views.administrator_list),
    path('administrator/add/', views.administrator_add),
    path('administrator/delete/', views.administrator_delete),
    path('administrator/<int:nid>/edit/', views.administrator_edit),
    path("attendancerate/", views.attendancerate),
    path("teacher_login/", views.teacher_login),
    path("teacher_show/", views.teacher_show),
    path("sign_in_start/", views.sign_in_start),
    path("sign_student/", views.sign_student),
]
