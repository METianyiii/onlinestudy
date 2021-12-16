import time

from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.user.models import Student, StudentInfo, Teacher, LearningBehavior, StartLive


@csrf_exempt
def studentLogin(request):
    if request.method == "GET":
        return render(request, 'user/studentLogin.html', locals())
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        identity = request.POST.get("identity")
        student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
        teacher = Teacher.objects.filter(Q(username=username) | Q(email=username)).first()
        # studentEmail = Student.objects.filter(email=username).first()
        if identity == "0":
            if student:
                if student.password == password:
                    request.session["username"] = username
                    request.session.set_expiry(3600 * 24)
                    student = Student.objects.filter(Q(username=username) | Q(email=username)).first()
                    LearningBehavior.objects.create(remoteID=request.META['REMOTE_ADDR'], loginTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), stu=student)
                    return redirect("/student/index/")
                else:
                    message = "密码错误"
                    return render(request, 'user/studentLogin.html', locals())
            else:
                message = "用户名或邮箱不存在"
                return render(request, 'user/studentLogin.html', locals())
        elif identity == "1":
            if teacher:
                if teacher.password == password:
                    request.session["teacherUsername"] = username
                    request.session.set_expiry(3600 * 24)
                    return redirect("/teacher/course/")
                else:
                    message = "密码错误"
                    return render(request, 'user/studentLogin.html', locals())
            else:
                message = "用户名或邮箱不存在"
                return render(request, 'user/studentLogin.html', locals())


@csrf_exempt
def studentRegister(request):
    if request.method == "GET":
        return render(request, 'user/studentRegister.html', locals())
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        student = Student.objects.filter(username=username).first()
        studentEmail = Student.objects.filter(email=email).first()

        if student:
            message = "用户名已存在"
            return render(request, 'user/studentRegister.html', locals())
        elif studentEmail:
            message = "邮箱已存在"
            return render(request, 'user/studentRegister.html', locals())
        elif password != password2:
            message = "密码不一样"
            return render(request, 'user/studentRegister.html', locals())
        else:
            student = Student.objects.create(username=username, email=email, password=password)
            StudentInfo.objects.create(student=student)
            request.session["username"] = username
            request.session.set_expiry(3600 * 24)
            LearningBehavior.objects.create(remoteID=request.META['REMOTE_ADDR'],
                                            loginTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), stu=student)
            return redirect("/student/index/")

def logout(request):
    identity = request.GET.get("identity")
    if identity == "0":
        request.session["username"] = None
        return redirect("user:studentLogin")
    elif identity == "1":
        request.session["teacherUsername"] = None
        return redirect("user:studentLogin")


@csrf_exempt
def teacherRegister(request):
    username = request.POST.get("username", '')
    email = request.POST.get("email", '')
    password = request.POST.get("password", '')
    password2 = request.POST.get("password2", '')
    teacher = Teacher.objects.filter(username=username).first()
    studentEmail = Teacher.objects.filter(email=email).first()
    if request.method == "POST":
        if teacher:
            message = "教师已存在"
            return render(request, 'user/studentRegister.html', locals())
        elif studentEmail:
            message = "邮箱已存在"
            return render(request, 'user/studentRegister.html', locals())
        elif password != password2:
            message = "密码不一样"
            return render(request, 'user/studentRegister.html', locals())
        else:
            teacher = Teacher.objects.create(username=username, email=email, password=password)
            StartLive.objects.create(tea=teacher)
            request.session["teacherUsername"] = username
            request.session.set_expiry(3600 * 24)
            return redirect("/teacher/course/")
    elif request.method == "GET":
        return render(request, 'user/teacherRegister.html', locals())
