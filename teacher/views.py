from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from crm import models
from django.views.decorators.csrf import csrf_exempt
from dlib_fase import settings
import json
from student import utils


@csrf_exempt
def teacher_info_uploadPicFile(request):
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


def teacher_info(request):
    tc_info = models.UserProfile.objects.get(email=request.user)
    return render(request, "teacher/tc_person_info.html", {"tc_info": tc_info})


def my_class_list(request):
    if request.method == "POST":
        print(request.POST)
        course_name = request.POST.get("class_name")
        course_num = request.POST.get("class_num")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        class_obj = models.ClassList()
        class_obj.course_name = course_name
        class_obj.semester = course_num
        class_obj.start_date = start_time
        class_obj.end_date = end_time
        class_obj.save()
        class_obj.teacher.add(request.user)
    return render(request, "teacher/my_class_list.html",{"from_url":request.path})


def course_records(request, class_obj_id):
    class_name = models.ClassList.objects.get(id=class_obj_id)
    print(class_name)
    course_obj = models.CourseRecord.objects.filter(from_class=class_obj_id)
    if request.method == "POST":
        print(request.POST.get("outlines"))
        if request.POST.get("outlines") is not None:
            outlines = request.POST.get("outlines")
            day_num = request.POST.get("day_num")
            course_record_obj = models.CourseRecord()
            course_record_obj.from_class = class_name
            course_record_obj.day_num = day_num
            course_record_obj.outlines = outlines
            course_record_obj.save()
        else:
            class_name.course_end_time = int(request.POST.get("course_end_time"))
            class_name.sign_end_time = int(request.POST.get("sign_end_time"))
            class_name.save()
    return render(request, "teacher/course_record.html",{"course_obj": course_obj,
                                                         "class_name":class_name})


@csrf_exempt
def teacher_sign(request, cource_record_id):
    course_record = models.CourseRecord.objects.get(id=cource_record_id)
    if request.method == "POST" and request.is_ajax():
        if request.POST.get("is_end") == "true":
            course_record.state = 0
            course_record.save()
    student = course_record.from_class.studenttoclass_set.all()
    if course_record.state == 2:
        for stu in student:
            try:
                print(stu.student)
                sign_record = models.SignRecord()
                sign_record.student = stu.student
                sign_record.attendance = 3
                sign_record.course_record = course_record
                sign_record.save()
            except:
                print("已有记录")
        course_record.state = 1
        course_record.start_sign_time =datetime.now()
        course_record.save()
    sign_record = course_record.signrecord_set.all().values("student__name", "attendance")
    sign_obj = {"signed":0,"late":0,"early_leave":0,"not_arrive":0,"sign_end_time":20,"course_end_time":120,
                "course_start_time": 0}
    for sign_record_colum in sign_record:
        if sign_record_colum["attendance"] == 3:
            sign_obj["not_arrive"] += 1
        if sign_record_colum["attendance"] == 2:
            sign_obj["early_leave"] += 1
        if sign_record_colum["attendance"] == 1:
            sign_obj["late"] += 1
        if sign_record_colum["attendance"] == 0:
            sign_obj["signed"] += 1
    sign_obj["sign_end_time"] = course_record.from_class.sign_end_time
    sign_obj["course_end_time"] = course_record.from_class.course_end_time
    time = course_record.start_sign_time
    time_obj = {"hour":time.hour,"minute":time.minute,"second":time.second}
    sign_obj["course_start_time"] = time_obj
    return render(request, "teacher/teacher_sign.html", {"sign_record": sign_record, "sign_obj":sign_obj})


def course_view(request,class_obj_id):
    course_count = models.CourseRecord.objects.filter(from_class_id=class_obj_id).all()
    sign_view_data = {"late":[],"not_arrive":[],"early_leave":[],"signed":[]}
    sign_view_data2 = {"late": [], "not_arrive": [], "early_leave": [], "signed": []}
    data_x = []
    data_x2 = []
    student_obj = models.Student.objects.filter(studenttoclass__enrolled_class_id=class_obj_id).all()
    for i in range(len(student_obj)):
        data_x2.append(student_obj[i].user.name)
        sign_view_data2["signed"].append(student_obj[i].signrecord_set.
                                         filter(attendance=0,course_record__from_class_id=class_obj_id).count())
        sign_view_data2["late"].append(student_obj[i].signrecord_set.
                                       filter(attendance=1,course_record__from_class_id=class_obj_id).count())
        sign_view_data2["early_leave"].append(student_obj[i].signrecord_set
                                              .filter(attendance=2,course_record__from_class_id=class_obj_id).count())
        sign_view_data2["not_arrive"].append(student_obj[i].signrecord_set.
                                             filter(attendance=3,course_record__from_class_id=class_obj_id).count())
    for i in range(len(course_count)):
        data_x.append(course_count[i].id)
        sign_view_data["signed"].append(course_count[i].signrecord_set.filter(attendance=0).count())
        sign_view_data["late"].append(course_count[i].signrecord_set.filter(attendance=1).count())
        sign_view_data["early_leave"].append(course_count[i].signrecord_set.filter(attendance=2).count())
        sign_view_data["not_arrive"].append(course_count[i].signrecord_set.filter(attendance=3).count())
    print(sign_view_data2)
    print(data_x2)
    return render(request,"teacher/course_view.html",{"sign_data":sign_view_data,
                                                      "data_x":data_x,
                                                      "sign_data2":sign_view_data2,
                                                      "data_x2":data_x2})
