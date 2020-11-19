from django import template
from django.utils.safestring import mark_safe
from crm import models
register = template.Library()


@register.simple_tag
def build_state(course_obj, request_user):
    ele = ''''''
    sign_state = models.SignRecord.objects.get(course_record_id=course_obj.id,student__user=request_user).attendance
    if course_obj.state == 1 and sign_state == 3:
        ele = '''<p><a href="/student/student_sign/%s/">签到</a></p>''' % course_obj.id
    elif sign_state == 0:
        ele = '''<p>已完成签到</p>'''
    elif sign_state == 1:
        ele = '''<p>迟到</p>'''
    elif sign_state == 2:
        ele = '''<p>早退</p>'''
    elif sign_state == 3 and course_obj.state == 0:
        ele = '''<p>缺勤</p>'''
    elif course_obj.state == 2:
        ele = '''<p>未开始</p>'''
    return mark_safe(ele)

