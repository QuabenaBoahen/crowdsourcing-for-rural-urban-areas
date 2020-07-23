import datetime as dt
from datetime import datetime
import random
from django import template


register = template.Library()


@register.filter(name='random_integer')
def random_integer(min, max):
    return str(random.randint(min, max))


@register.filter(name='days_since_deployment')
def days_since_deployment(deployment_date):
    total_days_since_deployment = ''
    date_format = '%Y-%m-%d'
    current_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), date_format)
    formatted_deployment_date = datetime.strptime(dt.datetime.strptime(deployment_date, '%d.%m.%Y').strftime('%Y-%m-%d'), date_format)
    date_diff = current_date - formatted_deployment_date
    if date_diff.days < 1:
        total_days_since_deployment = 'today'
    if date_diff.days == 1:
        total_days_since_deployment = str(date_diff.days) + " day ago"
    if date_diff.days > 1:
        total_days_since_deployment = str(date_diff.days) + " days ago"
    return total_days_since_deployment


