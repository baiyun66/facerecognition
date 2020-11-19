from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class Student(models.Model):
    student_num = models.CharField(max_length=32, blank=True, null=True, help_text="请用真实学号(工号)")
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True, null=True, help_text="请用真实姓名")
    qq = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", blank=True, null=True)
    sex_choices = ((0, "男"), (1, "女"),)
    sex = models.SmallIntegerField(choices=sex_choices, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "学生信息表"
        verbose_name_plural = "学生信息表"


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "学生标签表"
        verbose_name_plural = "学生标签表"


class ClassList(models.Model):
    course_name = models.CharField(verbose_name="班级名", max_length=255, unique=True, null=True)
    start_date = models.DateTimeField(verbose_name="开班日期")
    end_date = models.DateTimeField(verbose_name="结业日期", blank=True, null=True)
    semester = models.PositiveSmallIntegerField(verbose_name="学期")
    teacher = models.ManyToManyField("UserProfile")
    sign_end_time = models.SmallIntegerField(blank=True, null=True, default=20)
    course_end_time = models.SmallIntegerField(blank=True, null=True, default=120)

    def __str__(self):
        return "%s %s" % (self.course_name, self.semester)

    class Meta:
        unique_together = ('course_name', 'semester')
        verbose_name = "班级表"
        verbose_name_plural = "班级表"


class StudentTOClass(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey("ClassList", on_delete=models.CASCADE, verbose_name="所在班级")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.student, self.enrolled_class)

    class Meta:
        unique_together = ("student", "enrolled_class")
        verbose_name = "学生班级表"
        verbose_name_plural = "学生班级表"


class CourseRecord(models.Model):
    from_class = models.ForeignKey("ClassList", verbose_name="班级", on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    has_sign = models.BooleanField(default=True)
    outlines = models.TextField(verbose_name="本节课大纲")
    date = models.DateTimeField(auto_now_add=True)
    start_sign_time = models.DateTimeField(blank=True, null=True)
    state_choices = ((0, "已签到"),
                     (1, "正在签到"),
                     (2, "未开始"),)
    state = models.SmallIntegerField(choices=state_choices, default=2)

    def __str__(self):
        return "%s  %s" % (self.from_class, self.day_num)

    class Meta:
        unique_together = ("from_class", "day_num")
        verbose_name = "课程记录表"
        verbose_name_plural = "课程记录表"


class SignRecord(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    course_record = models.ForeignKey("CourseRecord", on_delete=models.CASCADE)
    attendance_choices = ((0, "已签到"),
                          (1, "迟到"),
                          (2, "早退"),
                          (3, "缺勤"),)
    attendance = models.SmallIntegerField(choices=attendance_choices, default=3)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.student, self.course_record)

    class Meta:
        unique_together = ('student', 'course_record')
        verbose_name = "课程签到记录表"
        verbose_name_plural = "课程签到记录表"


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        self.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role", blank=True)
    password = models.CharField(_('password'), max_length=128, help_text=mark_safe('''<a href='password/'>修改密码</a>'''))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):

        return self.is_admin

    class Meta:
        verbose_name = "账号表"
        verbose_name_plural = "帐号表"


class Role(models.Model):
    name = models.CharField(max_length=32, unique=True)
    menus = models.ManyToManyField("Menu")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = "角色表"


class Menu(models.Model):
    name = models.CharField(max_length=32)
    url_type_choices = ((0, "alias"), (1, "absolute_url"))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
