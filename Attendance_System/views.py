import pandas as pd
from Attendance_System.forms import RegistrationForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from Attendance_System import models
import time
from . import models
from Attendance_System.models import Class, Course, CollegeDay, Lecturer, Student, Semester, Profile, Admin, Attendance
# from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from  django.core.files.storage import FileSystemStorage
from django.http.response import JsonResponse
# from Attendance_System.forms import UserForm, RegisterForm, RegistrationForm

def exist_login(request):
    try:
        username=request.session.get('username')
        flag=request.session.get('flag')

        if flag=="student":
            users=User.objects.filter(username=username).first()
            return Student.objects.filter(user=users).exists()
        elif flag=='teacher':
            users = User.objects.filter(username=username).first()
            return Lecturer.objects.filter(user=users).exists()
        else:
            return Admin.objects.filter(username=username).exists()
    except:
        return redirect("/accounts/login/")
def logout(request):
    request.session.flush()
    return redirect("/accounts/login/")
def login(request):

    if request.method=='POST':
                flag=request.POST.get("flag")
                username=request.POST.get("username")
                password=request.POST.get("password")
                print(username)
                print(password)
                if flag=='student':
                    user_demo = User.objects.filter(username=username).first()
                    demo=Student.objects.filter(user=user_demo)
                    if len(demo)==0:
                        return JsonResponse({"flag": "Login failed"})
                    else:
                        demo = Student.objects.filter(user=user_demo).first()
                        if demo.user.password==password:
                            request.session['username']=username
                            request.session['flag']=flag
                            return JsonResponse({"flag":1,"url":"/sign_student/"})
                        else:
                            return JsonResponse({"flag":"Login failed"})

                elif flag=='teacher':
                    user_demo=User.objects.filter(username=username).first()
                    demo = Lecturer.objects.filter(user=user_demo)
                    if len(demo) == 0:
                        return JsonResponse({"flag": "Login failed"})
                    else:
                        demo = Lecturer.objects.filter(user=user_demo).first()
                        print(demo)
                        if demo.user.password == password:
                            request.session['username'] = username
                            request.session['flag'] = flag
                            return JsonResponse({"flag": 1, "url": "/teacher_login/"})
                        else:
                            return JsonResponse({"flag":"Login failed"})
                else:
                    demo = Admin.objects.filter(username=username,password=password)
                    if len(demo)!=0:
                        request.session['username'] = username
                        request.session['flag'] = flag
                        print({"flag": 1, "url": "/administrator/list/"})
                        return JsonResponse({"flag": 1, "url": "/administrator/list/"})
                    else:
                        return JsonResponse({"flag":"Login failed"})
    else:
        return redirect("/accounts/login/")



def semester_list(request):
    if exist_login(request):
        queryset = models.Semester.objects.all()
        return render(request, "semesters_list.html", {'queryset': queryset})
    else:
        return redirect("/accounts/login/")

def semester_add(request):
    if exist_login(request):
        if request.method == "GET":
           return render(request, 'semesters_add.html')
        else:
            year = request.POST.get("year")
            semester=request.POST.get('semester')
            Semester.objects.create(year=year,semester=semester,Semester_id=semester)
            return redirect('/semester/list/')
    else:
        return redirect("/accounts/login/")


def semester_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        models.Semester.objects.filter(id=nid).delete()
        return redirect('/semester/list/')
    else:
        return redirect("/accounts/login/")


def semester_edit(request, nid):
    if exist_login(request):
        if request.method == "GET":
          row_object = models.Semester.objects.filter(id=nid).first()
          # print(row_object.id, row_object.name)
          return render(request, 'semesters_edit.html', {"row_object":row_object})
        else:
            year = request.POST.get("year")
            semester = request.POST.get('semester')
            models.Semester.objects.filter(id=nid).update(year=year,semester=semester)

            return redirect("/semester/list/")
    else:
        return redirect("/accounts/login/")

#---------------teacher-----------------------
import datetime
def lecturer_list(request):
    if exist_login(request):
        lect_list=Lecturer.objects.all()
        return render(request,"lecturer_list.html",context={"row_object":lect_list})
    else:
        return redirect("/accounts/login/")

def lecturer_add(request):
    if exist_login(request):
        if request.method=='GET':
            return render(request,"lecturer_add.html")
        else:
            dob=str(datetime.date.today())
            staff_id=request.POST.get("staff_id")
            username=request.POST.get("username")
            password="123456"
            demo=User.objects.create(password=password,username=username)
            Lecturer.objects.create(staff_id=staff_id,DOB=dob,user=demo)
            return redirect("/lecturer/list")
    else:
        return redirect("/accounts/login/")

def lecturer_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        userdom = models.Lecturer.objects.get(pk=nid)
        userdom.user.delete()
        userdom.delete()
        return redirect('/lecturer/list/')
    else:
        return redirect("/accounts/login/")


def lecturer_edit(request, nid):
    if exist_login(request):
        if request.method == "GET":
          row_object = models.Lecturer.objects.filter(id=nid).first()
          # print(row_object.id, row_object.name)
          return render(request, 'lecturer_edit.html', {"row_object":row_object})
        else:
            staff_id = request.POST.get("staff_id")
            username = request.POST.get("username")
            dob = str(datetime.date.today())
            users=Lecturer.objects.filter(id=nid).first().user
            users.username=username
            users.save()
            models.Lecturer.objects.filter(id=nid).update(DOB=dob,staff_id=staff_id,user=users)

            return redirect("/lecturer/list/")
    else:
        return redirect("/accounts/login/")


#-----------------end teacher-------------

#----------student------------
def student_list(request):
    if exist_login(request):
        lect_list=Student.objects.all()
        return render(request,"student_list.html",context={"row_object":lect_list})
    else:
        return redirect("/accounts/login/")

def student_add(request):
    if exist_login(request):
        if request.method=='GET':
            return render(request,"student_add.html")
        else:
            dob=str(datetime.date.today())
            student_id=request.POST.get("student_id")
            student_username=request.POST.get("username")
            password="123456"
            demo=User.objects.create(password=password,username=student_username)
            Student.objects.create(student_id=student_id,DOB=dob,user=demo)
            return redirect("/student/list")
    else:
        return redirect("/accounts/login/")

def student_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        userdom=models.Student.objects.get(pk=nid)
        userdom.user.delete()
        userdom.delete()
        return redirect('/student/list/')
    else:
        return redirect("/accounts/login/")


def student_edit(request, nid):
    if exist_login(request):
        if request.method == "GET":
          row_object = models.Student.objects.filter(id=nid).first()
          # print(row_object.id, row_object.name)
          return render(request, 'student_edit.html', {"row_object":row_object})
        else:
            student_id = request.POST.get("student_id")
            student_username = request.POST.get("username")
            dob = str(datetime.date.today())
            users=Student.objects.filter(id=nid).first().user
            users.username=student_username
            users.save()
            models.Student.objects.filter(id=nid).update(DOB=dob,student_id=student_id,user=users)

            return redirect("/student/list/")
    else:
        return redirect("/accounts/login/")
#-----------------end student----------------------


#-------------------class---------------------------
def class_list(request):
    if exist_login(request):
        lect_list=Class.objects.all()
        return render(request,"class_list.html",context={"row_object":lect_list})

    else:
        return redirect("/login/")

def class_add(request):
    if exist_login(request):
        if request.method=='GET':
            course_list=Course.objects.all()
            date_list=Semester.objects.all()
            teacher_list=Lecturer.objects.all()
            student_list=Student.objects.all()
            return render(request,"class_add.html",context={
                "course_list":course_list,
                "date_list":date_list,
                "teacher_list":teacher_list,
                "student_list":student_list
            })
        else:
            class_id=request.POST.get('class_id')
            number=50
            course_id=request.POST.get("course_id")
            course_demo=Course.objects.get(pk=course_id)
            semester_id=request.POST.get("semester_id")
            semester_demo=Semester.objects.get(pk=semester_id)
            teacher_id=request.POST.get("teacher_id")
            teacher_demo=Lecturer.objects.get(pk=teacher_id)
            lecturer_id=request.POST.get("teacher_id")
            lecturer_demo=Lecturer.objects.get(pk=lecturer_id)
            student_id_list=request.POST.getlist("student_id")
            student_list_demo=Student.objects.filter(pk__in=student_id_list)
            demo=Class.objects.create(Class_id=class_id,number=number,
                                 course=course_demo,semester=semester_demo,
                                 lecturer=lecturer_demo)
            demo.student.set(student_list_demo)
            return redirect("/class/list")
    else:
        return redirect("/login/")

def class_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        models.Class.objects.filter(id=nid).delete()
        return redirect('/class/list/')
    else:
        return redirect("/login/")


def class_edit(request, nid):
    if exist_login(request):
        if request.method == "GET":
          row_object = models.Class.objects.filter(id=nid).first()
          row_object_student=row_object.student.all()
          course_list = Course.objects.all()
          date_list = Semester.objects.all()
          teacher_list = Lecturer.objects.all()
          student_list = Student.objects.all()
          return render(request, "class_edit.html", context={
              "course_list": course_list,
              "date_list": date_list,
              "teacher_list": teacher_list,
              "student_list": student_list,
              "row_object": row_object,
              "row_object_student": row_object_student
          })

        else:
            class_id = request.POST.get('class_id')
            number = 50
            course_id = request.POST.get("course_id")
            course_demo = Course.objects.get(pk=course_id)
            semester_id = request.POST.get("semester_id")
            semester_demo = Semester.objects.get(pk=semester_id)
            teacher_id = request.POST.get("teacher_id")
            teacher_demo = Lecturer.objects.get(pk=teacher_id)
            lecturer_id = request.POST.get("teacher_id")
            lecturer_demo = Lecturer.objects.get(pk=lecturer_id)
            student_id_list = request.POST.getlist("student_id")
            student_list_demo = Student.objects.filter(pk__in=student_id_list)
            demo = Class.objects.create(Class_id=class_id, number=number,
                                        course=course_demo, semester=semester_demo,
                                        lecturer=lecturer_demo)
            demo.student.set(student_list_demo)
            return redirect("/class/list")
    else:
        return redirect("/login/")
#-------------end class---------------------------------










# Create your views here.
def index(request):
    semesters = Semester.objects.all()
    context = {"title":"my home page title",
               "content":"my home page content - I just changed",
               "semesters":semesters}
    return render(request, "index.html", context)



def info_list(request):
    if exist_login(request):
        data_list = User.objects.all()


        return render(request, "info_list.html", {'data_list':data_list})
    else:
        return redirect("/login/")


def info_add(request):
    if exist_login(request):
        if request.method == "GET":
            return render(request, 'info_add.html')

        id = request.POST.get('id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')

        User.objects.create(id=id, username=username, email=email, password=pwd)

        return redirect('/info/list/')
    else:
        return redirect("/login/")


def info_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        User.objects.filter(id=nid).delete()
        return redirect('/info/list/')
    else:
        return redirect("/login/")


def collegeday_list(request):
    if exist_login(request):
        collegedata = models.CollegeDay.objects.all()

        return render(request, "collegeday_list.html", {'collegedata': collegedata})
    else:
        return redirect("/login/")




def collegeday_add(request):
    if exist_login(request):
        if request.method == "GET":
           return render(request, 'collegeday_add.html')
        name = request.POST.get("name")

        models.CollegeDay.objects.create(name=name)
        return redirect('/course/list/')
    else:
        return redirect("/login/")

def collegeday_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        models.CollegeDay.objects.filter(id=nid).delete()
        return redirect('/collegeday/list/')
    else:
        return redirect("/login/")

#---------------------------course--------------------
def course_list(request):
    if exist_login(request):
        queryset = models.Course.objects.all()
        return render(request, "course_list.html", {'queryset': queryset})
    else:
        return redirect("/login/")

def course_add(request):
    if exist_login(request):
        if request.method == "GET":
            date = Semester.objects.all()
            return render(request, 'course_add.html',context={"date":date})
        else:
            id=int(time.time()*1000)
            name = request.POST.get("name")
            semester_id=request.POST.get('semester')
            demo_se=Semester.objects.get(pk=semester_id)
            Course.objects.create(Course_id=id,name=name,semester=demo_se)
            return redirect('/course/list/')
    else:
        return redirect("/login/")

def course_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        models.Course.objects.filter(id=nid).delete()
        return redirect('/course/list/')
    else:
        return redirect("/login/")

def course_edit(request, nid):
    if exist_login(request):
        if request.method == "GET":
          date=Semester.objects.all()
          row_object = models.Course.objects.filter(id=nid).first()
          # print(row_object.id, row_object.name)
          return render(request, 'course_edit.html', {"row_object":row_object,
                                                  "date":date})
        name = request.POST.get("name")
        semester_id = request.POST.get('semester_id')
        demo_se = Semester.objects.get(pk=semester_id)
        models.Course.objects.filter(id=nid).update(name=name,semester_id=demo_se)
        return redirect("/course/list/")
    else:
        return redirect("/login/")



class RegistrationView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')



def CustomRegistration(request):
    if exist_login(request):
        if request.method == "POST":
            username = request.POST.get("username")
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            email = request.POST.get("email")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            bio = request.POST.get("bio")
            website = request.POST.get("website")
            if password1 == password2:
                user = User.objects.create_user(username=username)
                user.first_name = firstname
                user.last_name = lastname
                user.email = email
                user.set_password(password1)
                user.save()
                profile = Profile(user=user)
                profile.bio = bio
                profile.website = website
                profile.save()
                return HttpResponseRedirect(request("login"))
            else:
                return render(request, "registration_success.html", {"message": "Password are not same"})

        return render(request, "registration_success.html")
    else:
        return redirect("/login/")
#----------------------文件上传----------
def file_upload2(request):
    if exist_login(request):
        if request.method == "POST" and request.FILES["myfile"]:
            myfile = request.FILES["myfile"]
            username=request.session['username']
            demo=Admin.objects.filter(username=username).first()
            file_demo=Profile.objects.create(user=demo,bio=myfile)
            #读取file_demo文件
            data=pd.read_excel(file_demo)
            print(data)
        else:
            return render(request,"upload_file.html")

    else:
        return redirect("/login/")
def add_students(demo):

    demos = User.objects.create(password=demo['password'], username=demo['student_username'])
    dmeo1=Student.objects.create(student_id=demo['student_id'], DOB=demo['dob'], user=demos)
def file_upload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        upload_file_url = fs.url(filename)
        excle_data = pd.read_excel(myfile)
        data = pd.DataFrame(excle_data)
        data.apply(add_students,axis=1)
        return redirect("/student/list/")
    return render(request, 'upload_file.html')


def sendEmail(request):
    if exist_login(request):
        users = User.objects.all()
        if request.method == "POST":
            subject = request.POST.get("subject")
            body = request.POST.get("body")
            receiver = User.objects.get(id = request.POST.get("user"))
            senderEmail = "gabriel_sl19798@hotmail.com"
            try:
                send_mail(subject, body, senderEmail, [receiver.email],
                          fail_silently=False)
                return render(request, "emailsending.html", {
                    "message": "email has been sent out",
                    "users": users
                })
            except:
                return render(request, "emailsending.html", {
                    "message": "email sending failed",
                    "users": users
                })
        return render(request, "emailsending.html", {
            "message": "",
            "users": users
        })


def administrator_list(request):
    if exist_login(request):
        queryset = models.Admin.objects.all()

        context = {
            'queryset':queryset
        }
        return render(request, "admin_list.html", context)
    else:
        return redirect("/login/")



def administrator_add(request):
    if exist_login(request):
        if request.method == "GET":
            return render(request, 'admin_add.html')

        username = request.POST.get('username')
        pwd = request.POST.get('pwd')

        Admin.objects.create(username=username,  password=pwd)

        #
        # from = AdminModelForm(data=request.POST)
        # if form.is_valid():
        #     form.save()

        return redirect('/administrator/list/')
    else:
        return redirect("/login/")

def administrator_delete(request):
    if exist_login(request):
        nid = request.GET.get('nid')
        models.Admin.objects.filter(id=nid).delete()
        return redirect('/administrator/list/')
    else:
        return redirect("/login/")


def administrator_edit(request, nid):
    if exist_login(request):
        if request.method == "GET":

          row_object = models.Student.objects.filter(id=nid).first()

          return render(request, 'admin_edit.html', {"row_object":row_object})
        name = request.POST.get("name")
        models.Admin.objects.filter(id=nid).update(username=name)

        return redirect("/administrator/list/")
    else:
        return redirect("/login/")


def attendancerate(request):

    post = get_object_or_404(CollegeDay, id=request.get('post_id'))
    if post.attendance_rate.filter(id=request.user.id).exists():
        post.attendance_rate.remove(request.user)
    else:
        post.attendance_rate.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[request.POST.get('post_id')]))


def student_detail(DetailView):
    model = Student
    template_name = 'student_detail.html'

#-----------------------------------------------------
def teacher_login(request):
    if exist_login(request):
        if request.method=='GET':
            username=request.session.get("username")
            users = User.objects.filter(username=username).first()
            teacher=Lecturer.objects.filter(user=users).first()
            class_list=teacher.lecturer_class.all()
            infos=[]

            for class_demo in class_list:
                info={
                    "courseid":class_demo.course.pk,
                    "course_name":class_demo.course.name,
                    "classid":class_demo.pk,
                    "class_name":class_demo.Class_id,
                    'semesterid':class_demo.semester.id,
                    "semester":str(class_demo.semester.year)+"----"+str(class_demo.semester.semester),
                    'student':[]
                }
                for item in class_demo.student.all():
                    print(item)
                    info['student'].append(item.user.username)

                infos.append(info)
            print(infos)
            return render(request,"course_list_teacher.html",context={
                "info_list":infos,
                "username":request.session.get("username")
            })

    else:
        return redirect("/login/")

def sign_in_start(request):
    if exist_login(request):
        if request.method == 'GET':
            username = request.session.get("username")
            users = User.objects.filter(username=username).first()
            teacher_demo = Lecturer.objects.filter(user=users).first()
            courseid=request.GET.get("courseid")
            course_demo=Course.objects.get(pk=courseid)
            class_id=request.GET.get("class_id")
            class_demo=Class.objects.get(pk=class_id)

            student_all=class_demo.student.all()
            for demo in student_all:
                Attendance.objects.create(lecturer=teacher_demo,
                                          course=course_demo,
                                           student=demo,
                                          attendance=0)
            return redirect("/teacher_login/")

    else:
            return redirect("/login/")


#---------------student sign-----------------

def sign_student(request):
    if exist_login(request):
        if request.method == 'GET':
            username = request.session.get("username")
            users = User.objects.filter(username=username).first()
            student_demo=Student.objects.filter(user=users).first()
            attenlist=Attendance.objects.filter(student=student_demo,attendance=0)
            attenlist_check=Attendance.objects.filter(student=student_demo,attendance=1)
            infos=[]
            check_infos=[]
            for demo in attenlist:
                info={
                    "att_id":demo.pk,
                    "teachername":demo.lecturer.user.username,
                    "coursename":demo.course.name,
                }
                infos.append(info)
            for demo in attenlist_check:
                info={
                    "att_id":demo.pk,
                    "teachername":demo.lecturer.user.username,
                    "coursename":demo.course.name,
                }
                check_infos.append(info)
            return render(request,"course_list_student.html",context={
                "info_list":infos,
                "check_infos":check_infos,
                "username": request.session.get("username")
            })
        else:
            attid=request.POST.get('attid')
            Attendance.objects.filter(pk=attid).update(attendance=1)
            return redirect("/sign_student/")
    else:
            return redirect("/login/")


def teacher_show(request):
    if exist_login(request):
        if request.method == 'GET':
            username = request.session.get("username")
            users = User.objects.filter(username=username).first()
            teacher = Lecturer.objects.filter(user=users).first()
            class_list = teacher.lecturer_class.all()
            infos = []
            student_sign_ratio=Attendance.objects.filter(lecturer=teacher)
            check_rat=Attendance.objects.filter(lecturer=teacher).values()
            data=pd.DataFrame(data=check_rat)
            data.drop(columns="collegeday_id",inplace=True)
            deal_data=data.groupby(by=['student_id','course_id']).count().reset_index()
            print(deal_data)
            student_id_list=list(set(list(deal_data['student_id'])))
            course_id_list=list(set(list(deal_data['course_id'])))
            check_info=[]
            for i in student_id_list:
                for j in course_id_list:

                        # check_s=0
                    all_number=deal_data.loc[(deal_data['course_id'] == j) & (deal_data['student_id'] == i), :].shape[0]

                    if all_number!=0:
                        check_demo={
                            "all":all_number,
                            "studentname":Student.objects.get(pk=i).user.username,
                            "course_name":Course.objects.get(pk=j).name,
                            "check_count":deal_data.loc[(deal_data['student_id']==i) & (deal_data['attendance']==1) &(deal_data['course_id']==j) ,:].shape[0],
                            "absent":deal_data.loc[(deal_data['student_id']==i) & (deal_data['attendance']==0) & (deal_data['course_id']==j),:].shape[0],
                            "radio":""

                        }
                        check_demo['radio']=str((round(check_demo['check_count']/check_demo['all']*100,2)))+"%"
                        print(check_demo)
                        check_info.append(check_demo)
            # print(data)
            for demo in student_sign_ratio:
                info={
                    "course":demo.course.name,
                   "semester":str(demo.course.semester.year)+"----"+str(demo.course.semester.semester),
                    "student_name":demo.student.user.username,
                    "attendace":demo.attendance
                }
                infos.append(info)
            return render(request,"teacher_show.html",{
                "info_list":infos,
                "check_info":check_info,
                "username": request.session.get("username")
            })

    else:
            return redirect("/login/")


