from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Lecturer(models.Model):
    staff_id = models.PositiveIntegerField()
    DOB = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Student(models.Model):
    student_id = models.PositiveIntegerField()
    DOB = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Semester(models.Model):
    Semester_id = models.PositiveIntegerField()
    year = models.IntegerField()
    semester = models.CharField(max_length=32)

    def __str__(self):
        return self.semester


class Course(models.Model):
    Course_id = models.PositiveIntegerField()
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.name


class Class(models.Model):
    Class_id = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE,related_name="lecturer_class")
    student = models.ManyToManyField(Student, related_name='class_student', null=True, blank=True)

    def __str__(self):
        return self.course.name



class CollegeDay(models.Model):
    date = models.DateField(auto_now_add=True)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ManyToManyField(Student, related_name='CollegeDay_student', null=True, blank=True)
    attendance_rate = models.ManyToManyField(User, related_name='User_attendance', null=True, blank=True)

    def __str__(self):
        return self.Class.course.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.FileField(upload_to="%y%m%d/")
    website = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Attendance(models.Model):
    lecturer=models.ForeignKey(Lecturer,on_delete=models.CASCADE,null=True,blank=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=False,blank=False)
    collegeday = models.ForeignKey(CollegeDay, on_delete=models.CASCADE,null=True,blank=True)
    attendance = models.IntegerField()



class Admin(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True)
