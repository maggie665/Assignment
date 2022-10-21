from django.contrib import admin

# Register your models here.
from Attendance_System.models import Class, CollegeDay, Course, Lecturer, Semester, Student, User, Admin, Attendance


admin.site.register(Class)
admin.site.register(CollegeDay)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.register(Admin)
admin.site.register(Attendance)