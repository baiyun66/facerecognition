# Generated by Django 2.2.5 on 2020-03-29 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, null=True, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=32)),
                ('password', models.CharField(help_text="<a href='password/'>修改密码</a>", max_length=128, verbose_name='password')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': '账号表',
                'verbose_name_plural': '帐号表',
            },
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_num', models.CharField(blank=True, max_length=64, null=True)),
                ('course_name', models.CharField(max_length=255, null=True, unique=True, verbose_name='班级名')),
                ('start_date', models.DateTimeField(verbose_name='开班日期')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='结业日期')),
                ('semester', models.PositiveSmallIntegerField(verbose_name='学期')),
                ('teacher', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '班级表',
                'verbose_name_plural': '班级表',
                'unique_together': {('course_name', 'semester')},
            },
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='第几节(天)')),
                ('has_sign', models.BooleanField(default=True)),
                ('outlines', models.TextField(verbose_name='本节课大纲')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('from_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='班级')),
            ],
            options={
                'verbose_name': '课程记录表',
                'verbose_name_plural': '课程记录表',
                'unique_together': {('from_class', 'day_num')},
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('url_type', models.SmallIntegerField(choices=[(0, 'alias'), (1, 'absolute_url')], default=0)),
                ('url_name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'verbose_name': '学生标签表',
                'verbose_name_plural': '学生标签表',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='请用真实姓名', max_length=32, null=True)),
                ('qq', models.CharField(max_length=64, unique=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('id_num', models.CharField(blank=True, max_length=64, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='常用邮箱')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('sex', models.SmallIntegerField(choices=[(0, '男'), (1, '女')], default=0)),
                ('tags', models.ManyToManyField(blank=True, to='crm.Tag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '学生信息表',
                'verbose_name_plural': '学生信息表',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('menus', models.ManyToManyField(to='crm.Menu')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='crm.Role'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='StudentTOClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('enrolled_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='所在班级')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Student')),
            ],
            options={
                'verbose_name': '学生班级表',
                'verbose_name_plural': '学生班级表',
                'unique_together': {('student', 'enrolled_class')},
            },
        ),
        migrations.CreateModel(
            name='SignRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.SmallIntegerField(choices=[(0, '已签到'), (1, '迟到'), (2, '早退'), (3, '缺勤')], default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.CourseRecord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.Student')),
            ],
            options={
                'verbose_name': '课程签到记录表',
                'verbose_name_plural': '课程签到记录表',
                'unique_together': {('student', 'course_record')},
            },
        ),
    ]