import re
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def qq_validate(value):
    phone_re = re.compile(r'^([1-9])[0-9]{4,10}$')
    if not phone_re.match(value):
        raise ValidationError('QQ号码格式错误')


class StudentForm(Form):
    _phone = u'手机号码'
    _stu_num = '学号5-20个字符'
    _qq = 'QQ'

    stu_num = fields.CharField(max_length=20,
                               min_length=5,
                               error_messages={'required': '学号不能为空',
                                               'min_length': '学号最少为5个字符',
                                               'max_length': '学号最多为20个字符'},
                               widget=widgets.TextInput(attrs={'class': "form-control",
                                                               'id': "stu_num",
                                                               'placeholder': _stu_num}))
    phone = fields.CharField(validators=[mobile_validate, ],
                             error_messages={'required': '手机不能为空'},
                             widget=widgets.TextInput(attrs={'class': "form-control",
                                                             'id': "phone",
                                                             'placeholder':_phone}))
    qq = fields.CharField(validators=[qq_validate, ],
                          widget=widgets.TextInput(attrs={'class': "form-control",
                                                          'id': "qq",
                                                          'placeholder': _qq}))

    email = fields.EmailField(required=False,
                              error_messages={'required': u'邮箱不能为空', 'invalid': u'邮箱格式错误'},
                              widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': u'邮箱'}))

    sex = fields.IntegerField(required=True,
                              error_messages={'required': u"性别不能为空"})
