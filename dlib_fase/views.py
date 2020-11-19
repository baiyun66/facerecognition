from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from crm import models
from django.views.decorators.csrf import csrf_exempt
from dlib_fase import settings
import json
import base64
from student import utils
import os
from dlib_fase import utils as real_person


def delete(request, id):
    print(request.GET.get('next', ''))
    url = request.GET.get('next', '')
    obj = None
    if "class" in url:
        obj = models.ClassList.objects.get(id=id)
    elif "course" in url:
        obj = models.CourseRecord.objects.get(id=id)
    if request.method == "POST":
        obj.delete()
        return redirect(url)
    return render(request, "delete.html",{"obj":obj,"from_url":url})


@csrf_exempt
def acc_face_login(request):
    error = ''
    url = "face_login"
    flag = 0
    user = None
    if request.method == "POST" and request.is_ajax():
        json_re = json.loads(request.body)
        imgRes = json_re['uploadImg']
        imgdata = base64.b64decode(imgRes)
        print(imgdata)
        fase_file = settings.STU_FACE_DATA
        for filename in os.listdir(fase_file):
            print(filename[0:-4])
            is_sim = utils.is_sim_people("%s/%s" % (settings.STU_FACE_DATA, str(filename)), imgdata)
            if is_sim:
                user = models.UserProfile.objects.get(email=filename[0:-4])
                flag = 1
                break
        if flag:
            try:
                login(request, user)
                print(user)
                role = user.roles.values('menus__url_name')
                url = role[0]["menus__url_name"]
                print("url1",url)

                msg = {"msg":  reverse(url)}
                return HttpResponse(json.dumps(msg))
            except:
                role = user.roles.values('menus__url_name')
                url = role[1]["menus__url_name"]
                print(url)
        else:
            error = 'Wrong face!'
    return render(request, "face_login.html", {"error": error, "to_url":url})



@csrf_exempt
def eye_login(request):
    error = ''
    url = "face_login"
    flag = 0
    user = None

    if request.method == "POST" and request.is_ajax():
        myfile = request.FILES.get('myfile')
        file_path = "./signdata/%s" % myfile.name
        delList = []
        delDir = "./signdata"
        delList = os.listdir(delDir)
        for f in delList:
            filePath = os.path.join(delDir, f)
            if os.path.isfile(filePath):
                os.remove(filePath)
        with open(file_path, 'wb+') as f:
            for chunk in myfile.chunks():
                f.write(chunk)
        flag,user = real_person.is_person(file_path)
        print(flag,user)
        if flag == 1:
            try:
                login(request, user)
                print(user)
                role = user.roles.values('menus__url_name')
                url = role[0]["menus__url_name"]
                print("url1", url)

                msg = {"msg": reverse(url)}
                return HttpResponse(json.dumps(msg))
            except:
                role = user.roles.values('menus__url_name')
                url = role[1]["menus__url_name"]
                print(url)
        else:
            error = '不符合要求'
            print("不符合要求")
            url = "acc_login"
            msg = {"msg": reverse(url)}
            return HttpResponse(json.dumps(msg))
    return render(request, "real_face.html", {"error": error, "to_url": url})


def acc_login(request):
    error = ''
    if request.method == "POST":
        _email = request.POST.get('email')
        _password = request.POST.get('password')
        print(_email,_password)
        user = authenticate(username=_email, password=_password)
        if user:
            print("user")
            login(request, user)
            try:
                role = user._meta.model.objects.filter(email=user).values("roles")[0]
                url = models.Role.objects.filter(id=role["roles"]).values('menus__url_name')
                return redirect(url[0]["menus__url_name"])
            except:
                role = user._meta.model.objects.filter(email=user).values("roles")[0]
                url = models.Role.objects.filter(id=role["roles"]).values('menus__url_name')
                return redirect(url[1]["menus__url_name"])
        else:
            error = 'Wrong Username or password!'
    return render(request, "login.html", {"error": error})


def acc_logout(request):
    logout(request)
    return redirect("/account/login/")


def acc_register(request):
    error = ''
    if request.method == "POST":
        _email = request.POST.get('registerEmail')
        _username = request.POST.get('registerUsername')
        _password = request.POST.get('registerPassword')
        print(_email, _password,_username,request.POST.get('teacher'))
        _role = models.Role.objects.get(name='学生')
        if request.POST.get('teacher'):
            _role = models.Role.objects.get(name='老师')
        print(_role)
        if _email and _username and _password:
            user = models.UserProfile()
            user.name = _username
            user.set_password(_password)
            user.email = _email
            user.save()
            user = models.UserProfile.objects.get(email=_email)
            user.roles.add(_role)
            if not request.POST.get('teacher'):
                print("加入学生")
                student = models.Student()
                student.user = user
                student.name = user.name
                student.email = user.email
                student.save()
            else:
                print("加入老师")
            return render(request, "login.html", {"error": error})
        else:
            error = "注册格式不正确"
    return render(request, "register.html", {"error": error})
