from django.urls import path

from Attendance_System.views import index

urlpatterns = [
    path("", index, name="home"),
    ]