# Generated by Django 2.2.5 on 2020-04-03 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_auto_20200403_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='course_end_time',
            field=models.SmallIntegerField(blank=True, default=120, null=True),
        ),
        migrations.AlterField(
            model_name='classlist',
            name='sign_end_time',
            field=models.SmallIntegerField(blank=True, default=20, null=True),
        ),
    ]