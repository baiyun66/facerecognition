from django.contrib import admin
from django.urls import path,re_path,include
from dlib_fase import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^account/face_login/', views.acc_face_login, name='face_login'),
    re_path(r'^account/eye_login/', views.eye_login, name='eye_login'),
    re_path(r'^account/login/', views.acc_login, name='acc_login'),
    re_path(r'^account/logout/', views.acc_logout, name='acc_logout'),
    re_path(r'^account/register/', views.acc_register, name='acc_register'),
    re_path(r'^delete/(\d+)/$', views.delete,name="delete"),
    re_path(r'^student/', include("student.urls")),
    re_path(r'^teacher/', include("teacher.urls"))

]
