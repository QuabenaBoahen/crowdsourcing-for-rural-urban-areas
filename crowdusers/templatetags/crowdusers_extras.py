import random
from django import template


register = template.Library()


@register.filter(name='random_integer')
def random_integer(min, max):
    return str(random.randint(min, max))


