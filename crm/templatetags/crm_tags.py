from django import template
from django.utils.safestring import mark_safe
register = template.Library()



def recursive_related_objs_lookup(objs):
    ul_ele = "<ul>"
    for obj in objs:
        li_ele = '''<li> %s: %s </li>'''% (obj._meta.verbose_name, obj.__str__().strip("<>"))
        ul_ele += li_ele

        for m2m_field in obj._meta.local_many_to_many:
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name)
            for o in m2m_field_obj.select_related():
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele +=li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele

        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())
                    if hasattr(accessor_obj, 'select_related'):
                        target_objs = accessor_obj.select_related()
                        sub_ul_ele = "<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj, related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                if hasattr(accessor_obj,'select_related'):
                    target_objs = accessor_obj.select_related()

                else:
                    print("one to one i guess:", accessor_obj)
                    target_objs = accessor_obj

                if len(target_objs) >0:
                    nodes = recursive_related_objs_lookup(target_objs)
                    ul_ele += nodes
    ul_ele += "</ul>"
    return ul_ele


@register.simple_tag
def display_obj_related(obj):
    objs = [obj,]
    if obj:
        model_class = obj._meta.model
        mode_name = obj._meta.model_name
        return mark_safe(recursive_related_objs_lookup(objs))



