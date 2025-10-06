from django import template

from utility.models import Service


register = template.Library()


@register.simple_tag
def get_services():
    return Service.objects.all()


@register.filter
def class_name(value):
    return value.__class__.__name__
