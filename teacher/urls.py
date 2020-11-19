from django.urls import re_path
from teacher import views
from django.views.static import serve
import os
from dlib_fase.settings import BASE_DIR

urlpatterns = [
    re_path(r'^my_class_list/$', views.my_class_list, name="my_class_list"),
    re_path(r'^course_records/(\d+)/$', views.course_records, name="course_records"),
    re_path(r'^course_view/(\d+)/$', views.course_view, name="course_view"),
    re_path(r'^teacher_sign/(\d+)/$', views.teacher_sign, name="teacher_sign"),
    re_path(r'^teacher_info/$', views.teacher_info, name="teacher_info"),
    re_path(r'^teacher_info/uploadPicFile/$', views.teacher_info_uploadPicFile, name="teacher_info_uploadPicFile"),
    re_path(r'^teacher_info/stu_face/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, 'stu_face')})
]
