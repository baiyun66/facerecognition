from django.http import HttpResponse
from django.shortcuts import render
from crm import models
from django.views.decorators.csrf import csrf_exempt
from dlib_fase import settings
import json
import base64
from student import utils, form


@csrf_exempt
def person_info_uploadPicFile(request):
    if request.method == 'POST':
        print(request.FILES)
        myFile = request.FILES.get("file", None)
        if myFile:
            print(myFile)
            dir = "%s/%s" % (settings.STU_FACE_DATA, str(request.user) + '.jpg')
            if utils.is_face(myFile):
                destination = open(dir,'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()
                msg ={"msg":"ok"}
                return HttpResponse(json.dumps(msg))
            else:
                return HttpResponse('图片不是人')
        else:
            return HttpResponse('没有图片')


def person_info(request):
    student = models.Student.objects.get(user=request.user)
    obj = form.StudentForm()
    if request.method == "POST":
        obj = form.StudentForm(request.POST)
        status = obj.is_valid()
        print(status)
        if status:
            student_obj = models.Student.objects.filter(user=request.user).all()[0]
            student_obj.sex = request.POST.get('sex')
            student_obj.phone = request.POST.get('phone')
            student_obj.qq = request.POST.get('qq')
            student_obj.student_num = request.POST.get('stu_num')
            student_obj.save()
            student = student_obj
        success_dict = obj.clean()
        print(success_dict)
        failed_dict = obj.errors.as_json()
        print(failed_dict)
    return render(request, "student/stu_person_info.html", {"obj": obj, "student":student})


def class_list(request):
    error = ''
    class_list_obj = models.ClassList.objects.filter(studenttoclass__student__user=request.user)
    if request.method == "POST":
        if request.POST.get("class_id") != '':
            stu_cla = models.StudentTOClass()
            class_obj = models.ClassList.objects.filter(id=request.POST.get("class_id"))
            print(class_obj)
            if len(class_obj) != 0:
                stu_cla.student = models.Student.objects.filter(user=request.user)[0]
                stu_cla.enrolled_class = class_obj[0]
                stu_cla.save()
            else:
                error = "错误班级号！"
    print(error)
    return render(request, "student/stu_class_list.html", {"class_list_obj": class_list_obj, "error": error})


def stu_course_records(request, class_obj_id):
    class_name = models.ClassList.objects.get(id=class_obj_id)
    print(class_name)
    course_obj = models.CourseRecord.objects.filter(from_class=class_obj_id)
    sign_obj = models.SignRecord.objects.filter(student__user=request.user, course_record__from_class__id=class_obj_id).all()
    class_sign_obj = {"signed":0,"late":0,"not_arrive":0,"early_leave":0}
    for sign_record in sign_obj:
        if sign_record.attendance == 0:
            class_sign_obj["signed"] += 1
        elif sign_record.attendance == 1:
            class_sign_obj["late"] += 1
        elif sign_record.attendance == 2:
            class_sign_obj["early_leave"] += 1
        else:
            class_sign_obj["not_arrive"] += 1
    return render(request, "student/stu_course_record.html", {"course_obj": course_obj,
                                                              "class_name": class_name,
                                                              "class_sign_obj":class_sign_obj})


@csrf_exempt
def student_sign(request, cource_record_id):
    cource_record = models.CourseRecord.objects.get(id=cource_record_id)
    class_obj = cource_record.from_class
    if request.method == "POST" and request.is_ajax():
        json_re = json.loads(request.body)
        imgRes = json_re['uploadImg']
        imgdata = base64.b64decode(imgRes)
        is_sim = utils.is_sim_people("%s/%s" % (settings.STU_FACE_DATA, str(request.user) + '.jpg'), imgdata)
        print("issum",is_sim)
        if is_sim:
            models.SignRecord.objects.filter(student__user=request.user,
                                             course_record_id=cource_record_id).update(attendance=0)
            return HttpResponse("签到成功")
        else:
            return HttpResponse("签到失败")
    return render(request, "student/student_sign.html", {"class_obj": class_obj})
