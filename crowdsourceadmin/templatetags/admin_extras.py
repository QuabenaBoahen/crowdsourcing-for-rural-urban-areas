from django import template
from crowdusers.models import *

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def list_report_nature(report_nature_string):
    report_nature_list_from_string = report_nature_string.split(',')
    report_nature_to_display = []
    for i in report_nature_list_from_string:
        report_nature = ReportNature.objects.get(pk=i).name
        report_nature_to_display.append(report_nature)
    return ', '.join(report_nature_to_display)
