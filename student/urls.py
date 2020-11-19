
from django.urls import re_path

from dlib_fase.settings import BASE_DIR
from student import views
from django.views.static import serve
import os
urlpatterns = [
    re_path(r'^class_list/$', views.class_list, name="class_list"),
    re_path(r'^person_info/$', views.person_info, name="person_info"),
    re_path(r'^person_info/uploadPicFile/$', views.person_info_uploadPicFile, name="person_info_uploadPicFile"),
    re_path(r'^stu_course_records/(\d+)/$', views.stu_course_records, name="stu_course_records"),
    re_path(r'^student_sign/(\d+)/$', views.student_sign, name="student_sign"),
    re_path(r'^person_info/stu_face/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, 'stu_face')})
]
